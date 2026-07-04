# Kubernetes Cost Optimizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A tool to discover and analyze Kubernetes cluster resources with cost optimization framework. Currently at MVP stage with resource discovery capabilities fully functional.

## Current Status

This is an MVP (Minimum Viable Product) release focused on resource discovery. See [Roadmap](#roadmap) for planned features.

### What Works Now
- Resource discovery and listing
- Configuration system with environment overrides
- Docker containerization
- CLI interface

### Planned for Future Releases
- Prometheus metrics integration
- Cost calculation and analysis
- Optimization recommendations
- Report export (JSON, CSV, HTML)
- Slack notifications

## Features

- **Cluster Analysis**: Discover and list Kubernetes resources across all namespaces
- **Resource Discovery**: Fast scanning of nodes, deployments, StatefulSets, DaemonSets, and pods
- **Configuration**: Environment variable support with YAML fallback
- **Multi-Platform**: Docker support for easy deployment
- **CLI Interface**: Simple command-line interface for resource queries

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Kubernetes cluster with Prometheus metrics
- Docker Desktop (for local testing) or an active Kubernetes cluster

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Kubernetes-Cost-Optimizer.git
cd Kubernetes-Cost-Optimizer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the scanner
k8s-cost scan
```

### Docker Quick Start

```bash
# Build the Docker image
docker build -t k8s-cost-optimizer .

# Run with Docker Compose (includes Prometheus)
docker-compose up -d

# View logs
docker-compose logs -f k8s-cost-optimizer
```

See [SETUP.md](SETUP.md) for detailed local development and Docker Desktop instructions.

## Usage

### Basic Commands

```bash
# Show version
k8s-cost version

# Scan cluster and generate report
k8s-cost scan

# Display current configuration
k8s-cost show-config
```

### Configuration

Configuration is loaded from `config/` directory with environment variable overrides:

```bash
# Environment variables (take precedence over config files)
export PROMETHEUS_URL=http://prometheus:9090
export K8S_CLUSTER_NAME=production
export LOG_LEVEL=INFO

# Run with custom configuration
k8s-cost scan
```

See `.env.example` for all available environment variables.

## Architecture

```
k8s_cost_optimizer/
├── clients/              # External integrations (K8s, Prometheus, Slack)
├── analysis/             # Cost analysis and recommendation engine
├── services/             # Business logic layer
├── models/               # Data models and schemas
├── exporters/            # Report generation (JSON, CSV, HTML)
├── promql/               # Prometheus query builder
├── engine/               # Cost calculation engine
├── utils/                # Helpers and utilities
└── config.py             # Configuration management
```

## Configuration

### YAML Configuration Files

- `config/config.yaml` - Main application configuration
- `config/pricing.yaml` - Cloud provider pricing data
- `config/logging.yaml` - Logging configuration

### Environment Variables

All configuration can be overridden via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `KUBECONFIG` | `~/.kube/config` | Path to Kubernetes config |
| `K8S_CLUSTER_NAME` | `production` | Cluster name for reporting |
| `PROMETHEUS_URL` | `http://localhost:9090` | Prometheus server URL |
| `PROMETHEUS_TIMEOUT` | `30` | Request timeout in seconds |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `REPORT_OUTPUT_DIR` | `./reports` | Output directory for reports |

## Security

⚠️ **Important**: This tool accesses sensitive cluster information. Always:

1. Use proper RBAC permissions
2. Never commit `.env` or kubeconfig files
3. Store credentials in secure vaults
4. Use read-only service accounts when possible
5. Restrict network access to the tool

See [SECURITY.md](SECURITY.md) for detailed security guidelines.

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=k8s_cost_optimizer

# Run specific test file
pytest tests/test_cli.py
```

## Development

### Setup Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install with development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black isort

# Run tests
pytest

# Format code
black k8s_cost_optimizer tests
isort k8s_cost_optimizer tests
```

### Project Structure

- `k8s_cost_optimizer/` - Main package
- `tests/` - Unit and integration tests
- `config/` - Configuration files
- `docs/` - Documentation
- `examples/` - Example outputs and usage

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

### Version 0.2.0 (Next)
- [ ] Prometheus metrics integration
- [ ] Basic cost calculation
- [ ] JSON report export

### Version 0.3.0
- [ ] CSV and HTML report export
- [ ] Cost recommendations engine
- [ ] Slack notifications

### Future Versions
- [ ] Multi-cloud support (AWS, GCP, Azure cost APIs)
- [ ] Machine learning for anomaly detection
- [ ] Cost forecasting and trend analysis
- [ ] Automated right-sizing recommendations
- [ ] Integration with cost management platforms
- [ ] Web UI dashboard
- [ ] Real-time alerting

## Troubleshooting

### Connection Issues

**Problem**: Cannot connect to Kubernetes
```bash
# Verify kubeconfig
export KUBECONFIG=/path/to/config
k8s-cost show-config

# Check cluster access
kubectl cluster-info
```

**Problem**: Cannot reach Prometheus
```bash
# Test Prometheus connectivity
curl http://prometheus:9090/-/healthy

# Update configuration
export PROMETHEUS_URL=http://your-prometheus:9090
```

### Permission Issues

**Problem**: Insufficient permissions
```bash
# Check service account permissions
kubectl auth can-i list deployments --as=system:serviceaccount:default:optimizer
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Author

**Pankaj Aswal**
- GitHub: [@iampankajaswal](https://github.com/iampankajaswal)

## Support

For issues, questions, or contributions, please:

1. Check [existing issues](https://github.com/yourusername/Kubernetes-Cost-Optimizer/issues)
2. Review [documentation](docs/)
3. Open a [new issue](https://github.com/yourusername/Kubernetes-Cost-Optimizer/issues/new)

## Acknowledgments

- Kubernetes community for excellent Python SDK
- Prometheus for metrics platform
- All contributors and testers
