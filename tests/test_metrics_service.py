from unittest.mock import MagicMock

from k8s_cost_optimizer.clients.prometheus import PrometheusClient
from k8s_cost_optimizer.services.metrics import MetricsService


def test_service_creation():

    client = MagicMock(spec=PrometheusClient)

    service = MetricsService(client)

    assert service.client is client


def test_cpu_usage():

    client = MagicMock(spec=PrometheusClient)

    expected = MagicMock()

    client.execute.return_value = expected

    service = MetricsService(client)

    result = service.cpu_usage("default")

    assert result is expected

    client.execute.assert_called_once()


def test_memory_usage():

    client = MagicMock(spec=PrometheusClient)

    expected = MagicMock()

    client.execute.return_value = expected

    service = MetricsService(client)

    result = service.memory_usage("default")

    assert result is expected

    client.execute.assert_called_once()
