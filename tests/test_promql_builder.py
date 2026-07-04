from k8s_cost_optimizer.promql import PromQLBuilder, QueryOptions


def test_cpu_query():
    builder = PromQLBuilder()

    query = builder.cpu_usage(
        QueryOptions(
            namespace="default",
            workload="nginx",
        )
    )

    assert "container_cpu_usage_seconds_total" in query
    assert 'namespace="default"' in query
