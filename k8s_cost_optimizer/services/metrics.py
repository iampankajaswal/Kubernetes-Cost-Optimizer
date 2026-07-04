from __future__ import annotations

from k8s_cost_optimizer.clients.prometheus import PrometheusClient
from k8s_cost_optimizer.promql import (PrometheusResult, PromQLBuilder,
                                       QueryOptions)


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

        options = QueryOptions(namespace=namespace)
        query = self.builder.cpu_usage(options=options)
        return self.client.execute(query)

    ##########################################################

    def memory_usage(
        self,
        namespace: str,
    ) -> PrometheusResult:

        options = QueryOptions(namespace=namespace)
        query = self.builder.memory_usage(options=options)
        return self.client.execute(query)

    ##########################################################

    def cpu_requests(
        self,
        namespace: str,
    ) -> PrometheusResult:

        options = QueryOptions(namespace=namespace)
        query = self.builder.cpu_requests(options=options)
        return self.client.execute(query)

    ##########################################################

    def memory_requests(
        self,
        namespace: str,
    ) -> PrometheusResult:

        options = QueryOptions(namespace=namespace)
        query = self.builder.memory_requests(options=options)
        return self.client.execute(query)

    ##########################################################

    def cpu_limits(
        self,
        namespace: str,
    ) -> PrometheusResult:

        options = QueryOptions(namespace=namespace)
        query = self.builder.cpu_limits(options=options)
        return self.client.execute(query)

    ##########################################################

    def memory_limits(
        self,
        namespace: str,
    ) -> PrometheusResult:

        options = QueryOptions(namespace=namespace)
        query = self.builder.memory_limits(options=options)
        return self.client.execute(query)
