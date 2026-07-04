#!/bin/bash
echo "==== TEST 6: Docker Run ===="
echo ""
echo "6.1. Run: docker run k8s-cost-optimizer:test version"
docker run --rm k8s-cost-optimizer:test version
echo ""
echo "6.2. Run: docker run k8s-cost-optimizer:test show-config"
docker run --rm k8s-cost-optimizer:test show-config | head -15
echo ""
echo "6.3. Run with environment variable override"
docker run --rm -e PROMETHEUS_URL="http://test:9090" k8s-cost-optimizer:test show-config | grep -A1 "prometheus"
