from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


class Config:
    """
    Loads configuration from YAML files with environment variable overrides.

    Environment variables take precedence over YAML config.

    Example:

        config = Config()
        prometheus_url = config.get("prometheus.url")
        # Or via env var: PROMETHEUS_URL=http://custom:9090
    """

    def __init__(self, config_dir: str = "config"):

        self.config_dir = Path(config_dir)
        self.data = {}
        self._load()

    def _load_yaml(self, filename: str) -> dict:

        file = self.config_dir / filename

        if not file.exists():
            return {}

        with open(file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _get_env_override(self, key: str) -> Any:
        """Get environment variable override for dotted config key."""
        # Convert config.prometheus.url to CONFIG_PROMETHEUS_URL
        env_key = "K8S_" + key.upper().replace(".", "_")
        return os.getenv(env_key)

    def _load(self):

        self.data = {}
        self.data.update(self._load_yaml("config.yaml"))
        self.data["pricing"] = self._load_yaml("pricing.yaml")
        self.data["logging"] = self._load_yaml("logging.yaml")

        # Apply environment variable overrides
        self._apply_env_overrides()

    def _apply_env_overrides(self):
        """Apply environment variable overrides to loaded config."""
        # Kubernetes cluster name
        if cluster_name := os.getenv("K8S_CLUSTER_NAME"):
            if "cluster" not in self.data:
                self.data["cluster"] = {}
            self.data["cluster"]["name"] = cluster_name

        # Prometheus URL
        if prom_url := os.getenv("PROMETHEUS_URL"):
            if "prometheus" not in self.data:
                self.data["prometheus"] = {}
            self.data["prometheus"]["url"] = prom_url

        # Prometheus timeout
        if prom_timeout := os.getenv("PROMETHEUS_TIMEOUT"):
            if "prometheus" not in self.data:
                self.data["prometheus"] = {}
            self.data["prometheus"]["timeout"] = int(prom_timeout)

        # Kubeconfig path
        if kubeconfig := os.getenv("KUBECONFIG"):
            if "kubernetes" not in self.data:
                self.data["kubernetes"] = {}
            self.data["kubernetes"]["kubeconfig"] = kubeconfig

        # Report output directory
        if report_dir := os.getenv("REPORT_OUTPUT_DIR"):
            if "report" not in self.data:
                self.data["report"] = {}
            self.data["report"]["output"] = report_dir

        # Log level
        if log_level := os.getenv("LOG_LEVEL"):
            if "logging" not in self.data:
                self.data["logging"] = {}
            self.data["logging"]["level"] = log_level

    def get(self, key: str, default: Any = None):

        value = self.data

        for part in key.split("."):

            if not isinstance(value, dict):
                return default

            value = value.get(part)

            if value is None:
                return default

        return value

    def reload(self):

        self._load()
