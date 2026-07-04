from __future__ import annotations

from dataclasses import dataclass
from .models import PromQLQuery
from typing import Optional


@dataclass(slots=True)
class QueryOptions:
    namespace: Optional[str] = None
    workload: Optional[str] = None
    pod: Optional[str] = None
    container: Optional[str] = None


class PromQLBuilder:
    """
    Builds PromQL queries used throughout Kubernetes Cost Optimizer.

    This class ONLY builds queries.
    It never executes them.

    The Prometheus client is responsible for execution.
    """

    def __init__(self):
        pass

    # -----------------------------------------------------
    # Helpers
    # -----------------------------------------------------

    def _selector(self, options: QueryOptions) -> str:
        labels = []

        if options.namespace:
            labels.append(f'namespace="{options.namespace}"')

        if options.workload:
            labels.append(f'pod=~"{options.workload}.*"')

        if options.pod:
            labels.append(f'pod="{options.pod}"')

        if options.container:
            labels.append(f'container="{options.container}"')

        return ",".join(labels)

    # -----------------------------------------------------
    # CPU
    # -----------------------------------------------------

    def cpu_usage(
        self,
        options: QueryOptions,
        window: str = "5m",
    ) -> PromQLQuery:

        selector = self._selector(options)

        query = (
        "sum("
        f'rate(container_cpu_usage_seconds_total{{{selector}}}[{window}])'
        ")"
    )

        return PromQLQuery(
        name="cpu_usage",
        description="Current CPU usage",
        expression=query,
    )

    def cpu_average(
        self,
        options: QueryOptions,
        window: str = "7d",
    ) -> PromQLQuery:

        selector = self._selector(options)

        query = (
        "sum("
        f'rate(container_cpu_usage_seconds_total{{{selector}}}[{window}])'
        ")"
    )

        return PromQLQuery(
        name="cpu_usage",
        description="Current CPU usage",
        expression=query,
    )

    def cpu_peak(
        self,
        options: QueryOptions,
        window: str = "7d",
    ) -> PromQLQuery:

        selector = self._selector(options)

        query = (
        "sum("
        f'rate(container_cpu_usage_seconds_total{{{selector}}}[{window}])'
        ")"
    )

        return PromQLQuery(
        name="cpu_usage",
        description="Current CPU usage",
        expression=query,
    )

    # -----------------------------------------------------
    # Memory
    # -----------------------------------------------------

    def memory_usage(
        self,
        options: QueryOptions,
    ) -> PromQLQuery:

        selector = self._selector(options)

        query = (
        "sum("
        f'rate(container_cpu_usage_seconds_total{{{selector}}}[{window}])'
        ")"
    )

        return PromQLQuery(
        name="cpu_usage",
        description="Current CPU usage",
        expression=query,
    )

    def memory_peak(
        self,
        options: QueryOptions,
        window: str = "7d",
    ) -> PromQLQuery:

        selector = self._selector(options)

        query = (
        "sum("
        f'rate(container_cpu_usage_seconds_total{{{selector}}}[{window}])'
        ")"
    )

        return PromQLQuery(
        name="cpu_usage",
        description="Current CPU usage",
        expression=query,
    )

    # -----------------------------------------------------
    # Requests
    # -----------------------------------------------------

    def cpu_requests(
        self,
        options: QueryOptions,
    ) -> PromQLQuery:

        selector = self._selector(options)

        query = (
        "sum("
        f'rate(container_cpu_usage_seconds_total{{{selector}}}[{window}])'
        ")"
    )

        return PromQLQuery(
        name="cpu_usage",
        description="Current CPU usage",
        expression=query,
    )

    def memory_requests(
        self,
        options: QueryOptions,
    ) -> PromQLQuery:

        selector = self._selector(options)

        query = (
        "sum("
        f'rate(container_cpu_usage_seconds_total{{{selector}}}[{window}])'
        ")"
    )

        return PromQLQuery(
        name="cpu_usage",
        description="Current CPU usage",
        expression=query,
    )

    # -----------------------------------------------------
    # Limits
    # -----------------------------------------------------

    def cpu_limits(
        self,
        options: QueryOptions,
    ) -> PromQLQuery:

        selector = self._selector(options)

        query = (
        "sum("
        f'rate(container_cpu_usage_seconds_total{{{selector}}}[{window}])'
        ")"
    )

        return PromQLQuery(
        name="cpu_usage",
        description="Current CPU usage",
        expression=query,
    )

    def memory_limits(
        self,
        options: QueryOptions,
    ) -> PromQLQuery:

        selector = self._selector(options)

        query = (
        "sum("
        f'rate(container_cpu_usage_seconds_total{{{selector}}}[{window}])'
        ")"
    )

        return PromQLQuery(
        name="cpu_usage",
        description="Current CPU usage",
        expression=query,
    )

    # -----------------------------------------------------
    # Replica Count
    # -----------------------------------------------------

    def replicas(
        self,
        namespace: str,
        deployment: str,
    ) -> PromQLQuery:

        query = (
        "sum("
        f'rate(container_cpu_usage_seconds_total{{{selector}}}[{window}])'
        ")"
    )

        return PromQLQuery(
        name="cpu_usage",
        description="Current CPU usage",
        expression=query,
    )

    # -----------------------------------------------------
    # Pod Count
    # -----------------------------------------------------

    def pod_count(
        self,
        namespace: str,
    ) -> PromQLQuery:

        query = (
        "sum("
        f'rate(container_cpu_usage_seconds_total{{{selector}}}[{window}])'
        ")"
    )

        return PromQLQuery(
        name="cpu_usage",
        description="Current CPU usage",
        expression=query,
    )

    def raw(
        self,
        expression: str,
    ) -> PromQLQuery:

        return PromQLQuery(
            name="raw",
            description="Raw PromQL",
            expression=expression,
        )
