from __future__ import annotations

import time
from typing import Optional

import requests

from k8s_cost_optimizer.promql import PrometheusResult, PromQLQuery


class PrometheusClient:
    """
    Prometheus HTTP API Client.
    """

    def __init__(
        self,
        url: str,
        timeout: int = 30,
    ):

        self.url = url.rstrip("/")
        self.timeout = timeout

    ##########################################################

    @property
    def instant_endpoint(self) -> str:

        return f"{self.url}/api/v1/query"

    ##########################################################

    @property
    def range_endpoint(self) -> str:

        return f"{self.url}/api/v1/query_range"

    ##########################################################

    def health(self) -> bool:

        try:

            response = requests.get(
                f"{self.url}/-/healthy",
                timeout=self.timeout,
            )

            return response.status_code == 200

        except Exception:

            return False

    ##########################################################

    def execute(
        self,
        query: PromQLQuery,
    ) -> PrometheusResult:

        start = time.perf_counter()

        response = requests.get(
            self.instant_endpoint,
            params={
                "query": query.expression,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        payload = response.json()

        end = time.perf_counter()

        return PrometheusResult(
            query=query,
            success=payload["status"] == "success",
            result_type=payload["data"]["resultType"],
            result=payload["data"]["result"],
            raw=payload,
            execution_time_ms=(end - start) * 1000,
        )

    ##########################################################

    def execute_range(
        self,
        query: PromQLQuery,
        start: str,
        end: str,
        step: str = "5m",
    ) -> PrometheusResult:

        timer = time.perf_counter()

        response = requests.get(
            self.range_endpoint,
            params={
                "query": query.expression,
                "start": start,
                "end": end,
                "step": step,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        payload = response.json()

        elapsed = time.perf_counter() - timer

        return PrometheusResult(
            query=query,
            success=payload["status"] == "success",
            result_type=payload["data"]["resultType"],
            result=payload["data"]["result"],
            raw=payload,
            execution_time_ms=elapsed * 1000,
        )
