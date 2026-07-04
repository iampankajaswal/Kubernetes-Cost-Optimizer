#!/bin/bash
echo "==== TEST 5: Docker Build ===="
echo ""
echo "Building Docker image..."
cd /Users/pankajaswal/Kubernetes-Cost-Optimizer
docker build -t k8s-cost-optimizer:test . 2>&1 | grep -E "Successfully|error|warning" | head -20
echo ""
echo "Verifying image exists:"
docker images k8s-cost-optimizer:test
