#!/bin/bash
echo "==== TEST 1: CLI Commands ===="
echo ""
echo "1.1. Version command"
k8s-cost version
echo ""
echo "1.2. Show config command"
k8s-cost show-config
echo ""
echo "1.3. Nodes command"
k8s-cost nodes | head -20
