# Quick Reference Guide

## Before Pushing to GitHub

```bash
# 1. Verify nothing sensitive will be committed
git status
git diff --cached

# 2. Run all checks locally
pytest tests/ -v
black --check k8s_cost_optimizer tests
isort --check-only k8s_cost_optimizer tests
flake8 k8s_cost_optimizer tests
bandit -r k8s_cost_optimizer

# 3. Verify .gitignore is working
git status --ignored | grep -E "\.env|\.venv|kubeconfig"

# 4. Search for leftover credentials
git diff --cached | grep -i "password\|secret\|token\|key"

# 5. Build Docker image
docker build -t k8s-cost-optimizer:latest .

# 6. Push when clean
git add .
git commit -m "Production-ready release"
git push -u origin main
```

---

## Local Testing

### Using Python Virtual Environment
```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with:
export KUBECONFIG=~/.kube/config
export K8S_CLUSTER_NAME=docker-desktop
export PROMETHEUS_URL=http://localhost:9090

# Run
k8s-cost version
k8s-cost show-config
k8s-cost scan
```

### Using Docker Compose
```bash
# Start
docker-compose up -d

# Run
docker-compose exec k8s-cost-optimizer k8s-cost scan

# Check logs
docker-compose logs -f k8s-cost-optimizer

# View reports
cat reports/cluster_analysis.json | jq .

# Stop
docker-compose down
```

### Using Docker Desktop Kubernetes
```bash
# Enable in Docker Desktop: Settings → Kubernetes

# Verify
kubectl config use-context docker-desktop
kubectl get nodes

# Create reports directory
mkdir -p reports

# Run scanner
export KUBECONFIG=~/.kube/config
export K8S_CLUSTER_NAME=docker-desktop
k8s-cost scan

# Results
ls reports/
```

---

## Critical Checks Before Release

### ✅ Must Pass All

```bash
# Test
[ $(pytest tests/ -q | grep -c "passed") -gt 0 ] && echo "Tests OK" || echo "TESTS FAILED"

# No secrets
! git diff --cached | grep -q "password\|secret\|token" && echo "Secrets OK" || echo "SECRETS FOUND"

# Format clean
black --check k8s_cost_optimizer tests --quiet && echo "Format OK" || echo "NEEDS BLACK"

# Imports sorted
isort --check-only k8s_cost_optimizer tests --quiet && echo "Imports OK" || echo "NEEDS ISORT"

# Linting
flake8 k8s_cost_optimizer tests --quiet && echo "Linting OK" || echo "LINTING FAILED"

# No obvious security issues
bandit -r k8s_cost_optimizer -q && echo "Security OK" || echo "SECURITY ISSUES"
```

---

## Files to Never Commit

```
.env                    # Environment variables with secrets
.env.local              # Local overrides
.env.*.local            # Environment-specific secrets
.venv/                  # Virtual environment
venv/                   # Virtual environment
kubeconfig              # Kubernetes credentials
kubeconfig.*            # Kubernetes configs
*.pem                   # Private keys
*.key                   # Private keys
*.crt                   # Certificates
*secret*                # Anything with "secret"
*credentials*           # Anything with "credentials"
.DS_Store               # macOS metadata
__pycache__/            # Python cache
.pytest_cache/          # Pytest cache
*.log                   # Log files
import.log              # Import timing
```

All these are covered by `.gitignore` ✓

---

## Environment Variables

```bash
# REQUIRED for production
export PROMETHEUS_URL=http://prometheus:9090
export K8S_CLUSTER_NAME=production

# OPTIONAL but recommended
export KUBECONFIG=/path/to/kubeconfig
export PROMETHEUS_TIMEOUT=30
export LOG_LEVEL=INFO
export REPORT_OUTPUT_DIR=./reports

# See .env.example for all options
cat .env.example
```

---

## Docker Commands

```bash
# Build
docker build -t k8s-cost-optimizer:latest .
docker build --no-cache -t k8s-cost-optimizer:latest .

# Run
docker run k8s-cost-optimizer:latest version
docker run -e PROMETHEUS_URL=http://host:9090 k8s-cost-optimizer:latest scan

# Compose
docker-compose up -d          # Start
docker-compose down           # Stop (keep data)
docker-compose down -v        # Stop (delete data)
docker-compose logs -f        # Live logs
docker-compose ps             # Status

# Scan for vulnerabilities
docker scan k8s-cost-optimizer:latest
# OR
trivy image k8s-cost-optimizer:latest
```

---

## Git Commands

```bash
# Review before commit
git status
git diff --cached

# Commit
git add .
git commit -m "Your message"

# Push
git push -u origin main

# View history
git log --oneline -10
git show HEAD

# Emergency: Remove file from history
git filter-branch --tree-filter 'rm -f .env' HEAD
git push --force-with-lease
```

---

## Kubernetes Commands

```bash
# Check context
kubectl config current-context
kubectl config use-context docker-desktop

# Verify connectivity
kubectl get nodes
kubectl cluster-info

# Check RBAC
kubectl auth can-i list nodes

# Port-forward Prometheus
kubectl port-forward -n default svc/prometheus 9090:9090

# View logs
kubectl logs -f deployment/k8s-optimizer
```

---

## Testing Commands

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=k8s_cost_optimizer

# Run specific test
pytest tests/test_cli.py -v

# Run with output
pytest tests/ -v -s

# Coverage report
pytest --cov=k8s_cost_optimizer --cov-report=html
open htmlcov/index.html
```

---

## Code Quality Commands

```bash
# Format code
black k8s_cost_optimizer tests

# Sort imports
isort k8s_cost_optimizer tests

# Lint
flake8 k8s_cost_optimizer tests

# Type checking
mypy k8s_cost_optimizer --ignore-missing-imports

# Security scan
bandit -r k8s_cost_optimizer

# Dependency audit
pip-audit
```

---

## Troubleshooting Commands

```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Clean cache
rm -rf __pycache__ .pytest_cache .mypy_cache
pip cache purge

# Docker cleanup
docker system prune -a
docker images prune
docker volumes prune

# Verify kubeconfig
export KUBECONFIG=~/.kube/config
kubectl get nodes

# Test Prometheus
curl http://localhost:9090/-/healthy
```

---

## One-Liner Checks

```bash
# All tests pass?
pytest tests/ -q && echo "✓" || echo "✗"

# All formatted?
black --check k8s_cost_optimizer tests && echo "✓" || echo "✗"

# All imports sorted?
isort --check-only k8s_cost_optimizer tests && echo "✓" || echo "✗"

# No linting issues?
flake8 k8s_cost_optimizer tests && echo "✓" || echo "✗"

# No security issues?
bandit -r k8s_cost_optimizer -q && echo "✓" || echo "✗"

# Nothing sensitive staged?
! git diff --cached | grep -q "password\|secret" && echo "✓" || echo "✗"

# Docker builds?
docker build -t test . >/dev/null 2>&1 && echo "✓" || echo "✗"
```

---

## Final Verification Script

```bash
#!/bin/bash
set -e

echo "🔍 Pre-push verification..."
echo ""

echo "✓ Running tests..."
pytest tests/ -q

echo "✓ Checking format..."
black --check k8s_cost_optimizer tests

echo "✓ Checking imports..."
isort --check-only k8s_cost_optimizer tests

echo "✓ Linting..."
flake8 k8s_cost_optimizer tests

echo "✓ Security scan..."
bandit -r k8s_cost_optimizer -q

echo "✓ Building Docker image..."
docker build -t k8s-cost-optimizer:test . > /dev/null

echo "✓ Checking for secrets..."
! git diff --cached | grep -q "password\|secret\|token"

echo ""
echo "✅ All checks passed! Ready to push."
```

Save as `scripts/pre-push.sh` and run: `bash scripts/pre-push.sh`

---

## Remember

- **Never commit credentials** - Always use `.env.example` as template
- **Always test locally first** - Use Docker Compose for quick testing
- **Review git diff before commit** - Catch surprises early
- **Run CI/CD checks** - GitHub Actions will verify everything
- **Keep documentation updated** - README, SETUP, SECURITY files are critical

---

For more details:
- 📖 [README.md](README.md) - Project overview
- 🚀 [SETUP.md](SETUP.md) - Setup instructions
- 🔐 [SECURITY.md](SECURITY.md) - Security guidelines
- ✅ [CHECKLIST.md](CHECKLIST.md) - Verification steps
- 📋 [PRODUCTION_REVIEW.md](PRODUCTION_REVIEW.md) - Detailed review
