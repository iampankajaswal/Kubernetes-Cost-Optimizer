from __future__ import annotations

from k8s_cost_optimizer.clients.prometheus import PrometheusClient
from k8s_cost_optimizer.promql import (
    PromQLBuilder,
    PrometheusResult,
)


class MetricsService:

    def __init__(
        self,
        prometheus: PrometheusClient,
    ):

        self.client = prometheus
        self.builder = PromQLBuilder()

    ##########################################################

    def cpu_usage(
        self,
        namespace: str,
    ) -> PrometheusResult:

        query = self.builder.cpu_usage(
            namespace=namespace,
        )

        return self.client.execute(query)

    ##########################################################

    def memory_usage(
        self,
        namespace: str,
    ) -> PrometheusResult:

        query = self.builder.memory_usage(
            namespace=namespace,
        )

        return self.client.execute(query)

    ##########################################################

    def cpu_requests(
        self,
        namespace: str,
    ) -> PrometheusResult:

        query = self.builder.cpu_requests(
            namespace=namespace,
        )

        return self.client.execute(query)

    ##########################################################

    def memory_requests(
        self,
        namespace: str,
    ) -> PrometheusResult:

        query = self.builder.memory_requests(
            namespace=namespace,
        )

        return self.client.execute(query)

    ##########################################################

    def cpu_limits(
        self,
        namespace: str,
    ) -> PrometheusResult:

        query = self.builder.cpu_limits(
            namespace=namespace,
        )

        return self.client.execute(query)

    ##########################################################

    def memory_limits(
        self,
        namespace: str,
    ) -> PrometheusResult:

        query = self.builder.memory_limits(
            namespace=namespace,
        )

        return self.client.execute(query)
