from unittest.mock import MagicMock, patch

from k8s_cost_optimizer.clients.kubernetes import KubernetesClient


@patch("k8s_cost_optimizer.clients.kubernetes.client.CoreV1Api")
@patch("k8s_cost_optimizer.clients.kubernetes.client.AppsV1Api")
@patch("k8s_cost_optimizer.clients.kubernetes.config.load_kube_config")
def test_connect(
    mock_load_kube_config,
    mock_apps_api,
    mock_core_api,
):
    mock_core = MagicMock()
    mock_core.list_namespace.return_value = MagicMock(items=[])

    mock_core_api.return_value = mock_core

    client = KubernetesClient()
    client.connect()

    assert client.is_connected() is True
    mock_load_kube_config.assert_called_once()
