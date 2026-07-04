from unittest.mock import MagicMock, patch

from k8s_cost_optimizer.clients.prometheus import PrometheusClient
from k8s_cost_optimizer.promql import PromQLBuilder, QueryOptions


@patch("k8s_cost_optimizer.clients.prometheus.requests.get")
def test_health(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    client = PrometheusClient("http://localhost:9090")
    assert client.health()


@patch("k8s_cost_optimizer.clients.prometheus.requests.get")
def test_up_query(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "data": {"resultType": "vector", "result": []},
    }
    mock_get.return_value = mock_response

    client = PrometheusClient("http://localhost:9090")
    builder = PromQLBuilder()
    query = builder.raw("up")
    result = client.execute(query)

    assert result.success
    assert result.result_type == "vector"
