from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class Config:
    """
    Loads configuration from YAML files.

    Example:

        config = Config()

        prometheus_url = config.get("prometheus.url")
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

    def _load(self):

        self.data = {}

        self.data.update(self._load_yaml("config.yaml"))

        self.data["pricing"] = self._load_yaml("pricing.yaml")

        self.data["logging"] = self._load_yaml("logging.yaml")

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
