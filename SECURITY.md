# Security Policy

## Overview

The Kubernetes Cost Optimizer accesses sensitive cluster information and credentials. This document outlines security best practices and guidelines.

## Sensitive Data

This tool handles:
- **Kubernetes credentials** (kubeconfig, service account tokens)
- **Cluster configuration** (network topology, resource allocations)
- **Pod information** (application names, deployments, resource usage)
- **Prometheus credentials** (authentication tokens if applicable)
- **Cost data** (cloud pricing, usage metrics)

## Security Best Practices

### 1. Credential Management

**DO:**
- ✅ Use environment variables for sensitive config
- ✅ Store credentials in secure vaults (HashiCorp Vault, AWS Secrets Manager)
- ✅ Use Kubernetes Secrets for in-cluster deployments
- ✅ Rotate service account tokens regularly
- ✅ Use unique service accounts per environment

**DON'T:**
- ❌ Hardcode credentials in YAML files
- ❌ Commit `.env`, `.env.local`, or kubeconfig files
- ❌ Share credentials via Slack, email, or version control
- ❌ Use overly permissive RBAC rules
- ❌ Store credentials in Docker image

### 2. RBAC (Role-Based Access Control)

Use the minimal required permissions. Example:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: k8s-optimizer-reader
rules:
# Read-only access to required resources
- apiGroups: [""]
  resources: ["nodes", "namespaces", "pods"]
  verbs: ["get", "list"]
- apiGroups: ["apps"]
  resources: ["deployments", "statefulsets", "daemonsets"]
  verbs: ["get", "list"]
- apiGroups: ["metrics.k8s.io"]
  resources: ["pods", "nodes"]
  verbs: ["get", "list"]
# Explicitly deny write operations
- apiGroups: [""]
  resources: ["pods", "nodes", "namespaces"]
  verbs: ["create", "update", "patch", "delete"]
  effect: Deny
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: k8s-optimizer
  namespace: k8s-optimizer
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: k8s-optimizer-reader
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: k8s-optimizer-reader
subjects:
- kind: ServiceAccount
  name: k8s-optimizer
  namespace: k8s-optimizer
```

### 3. Network Security

**For Local Development:**
- Run on localhost only
- Disable public access to Prometheus
- Use firewall to restrict access

**For Production:**
- Deploy in private network
- Use VPN or private link for access
- Enable network policies in Kubernetes
- Use TLS for all connections

```yaml
# Example NetworkPolicy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: k8s-optimizer-policy
  namespace: k8s-optimizer
spec:
  podSelector:
    matchLabels:
      app: k8s-optimizer
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: monitoring
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443  # HTTPS
    - protocol: TCP
      port: 9090  # Prometheus
```

### 4. Data Protection

**Report Handling:**
- ✅ Encrypt reports at rest
- ✅ Use HTTPS when transmitting reports
- ✅ Set appropriate file permissions (600 or 644)
- ✅ Delete reports after processing
- ✅ Audit access to reports

**Avoid:**
- ❌ Storing reports in version control
- ❌ Committing reports to git
- ❌ Sharing reports via unencrypted channels
- ❌ Long-term storage of sensitive metrics

Example setup:

```bash
# Set restrictive permissions
mkdir -p reports
chmod 700 reports

# Encrypt report directory
# macOS with APFS:
# System Preferences → Security & Privacy → Encrypt

# Linux with LUKS:
# sudo cryptsetup luksFormat /dev/device
# sudo cryptsetup luksOpen /dev/device reports
```

### 5. Code Security

**Dependency Management:**
```bash
# Scan for vulnerable dependencies
pip-audit

# Update dependencies regularly
pip install --upgrade pip
pip-cache-prune

# Use lock files in production
pip freeze > requirements.lock
pip install -r requirements.lock
```

**Code Scanning:**
```bash
# Scan for secrets in code
git secrets --scan

# Static analysis
bandit -r k8s_cost_optimizer/

# Type checking
mypy k8s_cost_optimizer/
```

### 6. Logging Security

**DO:**
- ✅ Log authentication events
- ✅ Log all API calls
- ✅ Include timestamps and user info
- ✅ Centralize logs to secure server

**DON'T:**
- ❌ Log credentials or tokens
- ❌ Log sensitive environment variables
- ❌ Store logs with other data
- ❌ Make logs publicly accessible

Configuration:

```yaml
# config/logging.yaml
logging:
  level: INFO
  format: json
  handlers:
    file:
      path: /var/log/k8s-optimizer/app.log
      maxBytes: 10485760  # 10MB
      backupCount: 5
    syslog:
      address: /dev/log
      facility: local0
  # Never log credentials
  filters:
    - redact_credentials
```

### 7. Container Security

**Docker Image Best Practices:**
```dockerfile
# Use specific base image version (never 'latest')
FROM python:3.11-slim

# Run as non-root user
RUN useradd -m -u 1000 optimizer
USER optimizer

# Use read-only filesystem where possible
RUN chmod -R a-w /app

# Don't run as root
# ❌ WRONG: USER root
# ✅ CORRECT: USER optimizer

# Scan image for vulnerabilities
# docker scan k8s-cost-optimizer:latest
# OR use Trivy
# trivy image k8s-cost-optimizer:latest
```

**Registry Security:**
- Use private Docker registries
- Enable image signing
- Scan images before deployment
- Use image pull secrets

### 8. Supply Chain Security

**Dependency Verification:**
```bash
# Check for supply chain attacks
pip install --require-hashes -r requirements.txt

# Generate hashes
pip freeze --require-hashes > requirements.lock
```

**GitHub Security:**
- ✅ Enable branch protection
- ✅ Require code reviews
- ✅ Use signed commits
- ✅ Enable GitHub security scanning
- ✅ Use GitHub Actions for CI/CD

## Incident Response

### If Credentials Are Leaked:

1. **Immediate** (0-5 minutes):
   - Stop the tool
   - Revoke leaked credentials
   - Check git history for exposure

2. **Short-term** (5-30 minutes):
   - Generate new credentials
   - Update all instances
   - Check audit logs for unauthorized access

3. **Long-term** (1-24 hours):
   - Post-mortem analysis
   - Update security procedures
   - Implement new controls
   - Notify stakeholders if needed

### How to Remove Secrets from Git History:

```bash
# Option 1: Use git-filter-branch (careful!)
git filter-branch --tree-filter 'rm -f sensitive_file' HEAD

# Option 2: Use BFG (recommended)
bfg --delete-files sensitive_file

# Option 3: Force push (only if repo is fresh)
git reset --hard HEAD~1
git push --force-with-lease

# Option 4: Using GitHub web interface
# Settings → Danger Zone → Purge sensitive data
```

## Audit and Monitoring

### Enable Audit Logging

**Kubernetes Audit:**
```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
# Log pod list operations at RequestResponse level
- level: RequestResponse
  resources: ["pods"]
  namespaces: ["k8s-optimizer"]
```

**Application Logs:**
```bash
# View logs with structured format
docker-compose logs k8s-cost-optimizer --follow

# Parse JSON logs
docker-compose logs k8s-cost-optimizer | jq '.level,.timestamp,.message'
```

## Compliance Considerations

### Data Residency
- Store data in compliant regions
- Check local data protection laws (GDPR, CCPA)
- Document data retention policies

### Access Control
- Implement least privilege principle
- Maintain audit trail of access
- Document who has access and why

### Encryption
- Use TLS 1.3+ for all network traffic
- Encrypt sensitive data at rest
- Use strong key management

## Security Scanning

**Run before each release:**

```bash
# Code analysis
bandit -r k8s_cost_optimizer/ -f json

# Dependency audit
pip-audit --desc --skip-editable

# SBOM generation
pip-licenses --format=json > sbom.json

# Secret detection
truffleHog filesystem . --json
```

## Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT** open a public issue
2. Email: [security@example.com](mailto:security@example.com)
3. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

We will acknowledge within 48 hours and provide timeline for patch.

## Security Checklist Before Production

- [ ] All credentials in environment variables
- [ ] `.gitignore` prevents secret commits
- [ ] RBAC permissions minimized
- [ ] Network policies configured
- [ ] Audit logging enabled
- [ ] TLS enabled for all connections
- [ ] Non-root user in containers
- [ ] Dependencies scanned for vulnerabilities
- [ ] Code scanning enabled (GitHub/GitLab)
- [ ] Secrets rotation policy defined
- [ ] Incident response plan documented
- [ ] Security review completed

## References

- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Docker Security](https://docs.docker.com/engine/security/)

