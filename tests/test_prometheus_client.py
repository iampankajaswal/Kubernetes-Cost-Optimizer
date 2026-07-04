from k8s_cost_optimizer.clients.prometheus import PrometheusClient
from k8s_cost_optimizer.promql import (
    PromQLBuilder,
    QueryOptions,
)


def test_health():

    client = PrometheusClient(
        "http://localhost:9090"
    )

    assert client.health()


def test_up_query():

    client = PrometheusClient(
        "http://localhost:9090"
    )

    builder = PromQLBuilder()

    query = builder.raw(
        "up"
    )

    result = client.execute(query)

    assert result.success
    assert result.result_type == "vector"
