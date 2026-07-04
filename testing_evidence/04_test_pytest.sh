#!/bin/bash
echo "==== TEST 4: Pytest Test Suite ===="
echo ""
cd /Users/pankajaswal/Kubernetes-Cost-Optimizer
pytest tests/ -v --tb=short
