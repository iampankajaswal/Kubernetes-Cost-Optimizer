# Setup Guide - Kubernetes Cost Optimizer

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Docker Desktop Setup](#docker-desktop-setup)
3. [Docker Compose Setup](#docker-compose-setup)
4. [Production Deployment](#production-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Local Development Setup

### Prerequisites

- Python 3.11 or higher
- pip package manager
- A Kubernetes cluster (local or remote)
- Prometheus instance with Kubernetes metrics

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/Kubernetes-Cost-Optimizer.git
cd Kubernetes-Cost-Optimizer
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure

Create a `.env` file in the project root:

```bash
# Copy from example
cp .env.example .env

# Edit with your values
# nano .env  # or your favorite editor
```

Example `.env` for local testing:

```bash
# Local Kubernetes (Docker Desktop)
KUBECONFIG=~/.kube/config
K8S_CLUSTER_NAME=docker-desktop

# Local Prometheus
PROMETHEUS_URL=http://localhost:9090
PROMETHEUS_TIMEOUT=30

# Logging
LOG_LEVEL=DEBUG
REPORT_OUTPUT_DIR=./reports

# Create reports directory
mkdir -p reports
```

### Step 5: Test Installation

```bash
# Verify installation
k8s-cost version

# Check configuration
k8s-cost show-config

# List cluster info
kubectl cluster-info

# Verify Prometheus connection
curl http://localhost:9090/-/healthy
```

### Step 6: Run Scanner

```bash
# Scan cluster
k8s-cost scan

# View generated reports
ls -la reports/
cat reports/cluster_analysis.json
```

---

## Docker Desktop Setup

### Prerequisites

- Docker Desktop installed
- Kubernetes enabled in Docker Desktop
- At least 4GB RAM allocated to Docker
- At least 2 CPU cores allocated to Docker

### Step 1: Enable Kubernetes

1. Open Docker Desktop
2. Go to **Preferences** → **Kubernetes**
3. Check **Enable Kubernetes**
4. Wait for status to show "kubernetes is running"

### Step 2: Verify Setup

```bash
# Check Docker Desktop K8s context
kubectl config get-contexts

# You should see: docker-desktop

# Switch to it (if needed)
kubectl config use-context docker-desktop

# Verify connectivity
kubectl get nodes

# You should see: docker-desktop   Ready    control-plane   ...
```

### Step 3: Install Prometheus (Optional but Recommended)

For local testing with Prometheus metrics:

```bash
# Using Helm (recommended)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack

# Or using kubectl manifest (simpler)
kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/main/bundle.yaml
```

Verify Prometheus is running:

```bash
# Check pods
kubectl get pods | grep prometheus

# Port-forward to local
kubectl port-forward -n default svc/prometheus 9090:9090

# Access it
open http://localhost:9090
```

### Step 4: Set Environment Variables

```bash
# For Docker Desktop Kubernetes
export KUBECONFIG=~/.kube/config
export K8S_CLUSTER_NAME=docker-desktop
export PROMETHEUS_URL=http://localhost:9090

# Optional
export LOG_LEVEL=DEBUG
mkdir -p reports
export REPORT_OUTPUT_DIR=./reports
```

### Step 5: Run the Tool

```bash
# Activate virtual environment
source venv/bin/activate

# Run scanner
k8s-cost scan

# Check output
cat reports/cluster_analysis.json | jq .
```

---

## Docker Compose Setup

### Prerequisites

- Docker installed
- Docker Compose installed (usually comes with Docker Desktop)
- At least 4GB available disk space

### Step 1: Prepare Configuration

The `docker-compose.yml` includes:
- Prometheus service
- k8s-cost-optimizer service
- Shared network for communication

```bash
# Review the docker-compose.yml
cat docker-compose.yml
```

### Step 2: Build Docker Image

```bash
# Build the image
docker build -t k8s-cost-optimizer:latest .

# Verify build
docker images | grep k8s-cost-optimizer
```

### Step 3: Start Services

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# You should see:
# NAME                    STATUS
# k8s-cost-prometheus     Up (healthy)
# k8s-cost-optimizer      Up
```

### Step 4: View Logs

```bash
# All logs
docker-compose logs -f

# Specific service
docker-compose logs -f k8s-cost-optimizer

# Prometheus logs
docker-compose logs -f prometheus
```

### Step 5: Access Services

```bash
# Prometheus UI
open http://localhost:9090

# Run tool commands
docker-compose exec k8s-cost-optimizer k8s-cost version

# Scan cluster
docker-compose exec k8s-cost-optimizer k8s-cost scan

# View reports (mounted locally)
ls reports/
cat reports/cluster_analysis.json | jq .
```

### Step 6: Stop Services

```bash
# Stop all services (keep data)
docker-compose stop

# Stop and remove (clean slate)
docker-compose down

# Remove volumes too
docker-compose down -v
```

---

## Production Deployment

### Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace k8s-optimizer

# Create service account
kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: k8s-optimizer
  namespace: k8s-optimizer
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: k8s-optimizer
rules:
- apiGroups: [""]
  resources: ["nodes", "namespaces", "pods", "pods/log"]
  verbs: ["get", "list"]
- apiGroups: ["apps"]
  resources: ["deployments", "statefulsets", "daemonsets"]
  verbs: ["get", "list"]
- apiGroups: ["metrics.k8s.io"]
  resources: ["pods", "nodes"]
  verbs: ["get", "list"]
EOF

# Bind role
kubectl create clusterrolebinding k8s-optimizer \
  --clusterrole=k8s-optimizer \
  --serviceaccount=k8s-optimizer:k8s-optimizer
```

### Deploy using Helm/Kustomize

```bash
# Kustomize example
kustomize build deployments/k8s-optimizer | kubectl apply -f -

# Or manual kubectl
kubectl apply -f deployments/k8s-optimizer.yaml
```

### Verify Production Deployment

```bash
# Check pod status
kubectl get pods -n k8s-optimizer

# View logs
kubectl logs -n k8s-optimizer -l app=k8s-optimizer -f

# Verify Prometheus metrics
kubectl exec -n k8s-optimizer k8s-optimizer-0 -- \
  curl http://prometheus:9090/-/healthy
```

---

## Troubleshooting

### Issue: Cannot Connect to Kubernetes

**Symptoms**: Error "Unable to connect to Kubernetes"

**Solutions**:

```bash
# 1. Check kubeconfig
echo $KUBECONFIG
ls -la ~/.kube/config

# 2. Verify current context
kubectl config current-context

# 3. Test connectivity
kubectl get nodes

# 4. Check permissions
kubectl auth can-i get nodes

# 5. If using Docker Desktop, ensure it's running
docker ps  # Should show docker-desktop resources
```

### Issue: Cannot Connect to Prometheus

**Symptoms**: Error "Failed to connect to Prometheus"

**Solutions**:

```bash
# 1. Check Prometheus URL
echo $PROMETHEUS_URL

# 2. Test connectivity
curl -v http://localhost:9090/-/healthy

# 3. If using Docker Compose
docker-compose logs prometheus
docker-compose exec prometheus curl http://localhost:9090/-/healthy

# 4. If using Kubernetes
kubectl port-forward -n default svc/prometheus 9090:9090
curl http://localhost:9090/-/healthy

# 5. Check firewall
telnet localhost 9090
```

### Issue: Permission Denied on Report Output

**Symptoms**: Error "Permission denied" when writing reports

**Solutions**:

```bash
# 1. Check directory permissions
ls -la reports/

# 2. Create directory with proper permissions
mkdir -p reports
chmod 755 reports

# 3. Or use absolute path
export REPORT_OUTPUT_DIR=/tmp/k8s-reports
mkdir -p $REPORT_OUTPUT_DIR
```

### Issue: Out of Memory (Docker)

**Symptoms**: Container crashes or exits

**Solutions**:

```bash
# 1. Check memory allocation
docker stats

# 2. Increase Docker Desktop memory
# Open Docker Desktop → Preferences → Resources
# Increase Memory to 6GB or more

# 3. Or specify limits in docker-compose
docker-compose -f docker-compose.yml up --compatibility
```

### Issue: Import Errors with Python

**Symptoms**: "ModuleNotFoundError: No module named..."

**Solutions**:

```bash
# 1. Verify virtual environment is activated
which python  # Should show /path/to/venv/bin/python

# 2. Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Check Python version
python --version  # Should be 3.11+

# 4. Reinstall from scratch
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Stale Docker Images

**Symptoms**: Old code still running

**Solutions**:

```bash
# 1. Rebuild without cache
docker build --no-cache -t k8s-cost-optimizer:latest .

# 2. Remove old images
docker rmi k8s-cost-optimizer:old-version

# 3. Clean up everything (careful!)
docker system prune -a
```

---

## Performance Tips

### Local Development

- Use `LOG_LEVEL=DEBUG` for detailed output
- Run with smaller cluster for faster scanning
- Cache results between runs

### Docker Compose

- Allocate adequate resources (4GB+ RAM, 2+ CPU)
- Use named volumes for faster I/O
- Mount reports directory locally for quick access

### Production

- Use in-cluster Prometheus (no network latency)
- Schedule scanner as CronJob for regular analysis
- Store reports in persistent volume

---

## Next Steps

1. Review [README.md](README.md) for features and usage
2. Check [SECURITY.md](SECURITY.md) for security best practices
3. Review [PRODUCTION_REVIEW.md](PRODUCTION_REVIEW.md) for production readiness
4. Explore configuration in `config/` directory
5. Run tests: `pytest`

---

## Getting Help

- Check logs: `docker-compose logs` or `kubectl logs`
- Enable debug logging: `LOG_LEVEL=DEBUG`
- Review configuration: `k8s-cost show-config`
- Open an issue on GitHub

