from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from k8s_cost_optimizer.promql.models import PromQLQuery


@dataclass(slots=True)
class PrometheusResult:
    """
    Result returned from Prometheus.
    """

    query: PromQLQuery
    success: bool
    result_type: str
    result: list[dict[str, Any]] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0
