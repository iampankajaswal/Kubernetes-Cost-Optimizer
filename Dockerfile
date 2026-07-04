# Multi-stage build for Kubernetes Cost Optimizer

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip install --user --no-cache-dir --no-warn-script-location -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LOG_LEVEL=INFO \
    PROMETHEUS_URL=http://prometheus:9090 \
    PROMETHEUS_TIMEOUT=30 \
    REPORT_OUTPUT_DIR=/reports

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash optimizer

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /usr/local

# Copy application code
COPY --chown=optimizer:optimizer k8s_cost_optimizer/ ./k8s_cost_optimizer/
COPY --chown=optimizer:optimizer config/ ./config/
COPY --chown=optimizer:optimizer pyproject.toml setup.py* ./

# Create reports directory
RUN mkdir -p /reports && chown optimizer:optimizer /reports

# Install application (as root, into /usr/local)
RUN pip install --no-cache-dir --no-warn-script-location .

# Switch to non-root user
USER optimizer

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD k8s-cost version || exit 1

# Default command
ENTRYPOINT ["k8s-cost"]
CMD ["--help"]

# Labels for metadata
LABEL maintainer="Pankaj Aswal" \
      description="Kubernetes Cost Optimizer - Analyze and optimize Kubernetes cluster costs" \
      version="0.1.0"
