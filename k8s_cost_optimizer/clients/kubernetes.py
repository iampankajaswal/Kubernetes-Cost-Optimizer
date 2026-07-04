from __future__ import annotations

from typing import List, Optional

from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException

from k8s_cost_optimizer.models.deployment import Deployment
from k8s_cost_optimizer.models.namespace import Namespace


class KubernetesClient:
    """
    Wrapper around Kubernetes Python SDK.

    Supports:

    - Local kubeconfig
    - In-cluster configuration
    - Namespace discovery
    - Deployment discovery
    - StatefulSets
    - DaemonSets
    - Pods
    - Nodes
    """

    def __init__(self):

        self.connected = False

        self.core: Optional[client.CoreV1Api] = None
        self.apps: Optional[client.AppsV1Api] = None

    ########################################################

    def connect(self):
        """
        Connect to Kubernetes using the local kubeconfig.
        If unavailable, fall back to in-cluster config.
        """

        try:

            config.load_kube_config()

        except ConfigException:

            config.load_incluster_config()

        self.core = client.CoreV1Api()
        self.apps = client.AppsV1Api()

        # Validate the connection
        self.core.list_namespace(limit=1)
        self.connected = True

    ########################################################

    def is_connected(self) -> bool:

        return self.connected

    ########################################################

    def cluster_version(self):

        version_api = client.VersionApi()

        return version_api.get_code()

    ########################################################

    def namespaces(self) -> List[Namespace]:

        namespaces = []

        response = self.core.list_namespace()

        for ns in response.items:

            namespaces.append(
                Namespace(
                    name=ns.metadata.name,
                    status=ns.status.phase,
                )
            )

        return namespaces

    ########################################################

    def nodes(self):

        nodes = []

        response = self.core.list_node()

        for node in response.items:

            nodes.append(
                {
                    "name": node.metadata.name,
                    "kernel": node.status.node_info.kernel_version,
                    "os": node.status.node_info.os_image,
                    "kubelet": node.status.node_info.kubelet_version,
                }
            )

        return nodes

    ########################################################

    def pods(self):

        pods = []

        response = self.core.list_pod_for_all_namespaces()

        for pod in response.items:

            pods.append(
                {
                    "namespace": pod.metadata.namespace,
                    "name": pod.metadata.name,
                    "status": pod.status.phase,
                    "node": pod.spec.node_name,
                }
            )

        return pods

    ########################################################

    def deployments(self) -> List[Deployment]:

        deployments = []

        response = self.apps.list_deployment_for_all_namespaces()

        for d in response.items:

            deployments.append(
                Deployment(
                    namespace=d.metadata.namespace,
                    name=d.metadata.name,
                    replicas=d.spec.replicas or 0,
                )
            )

        return deployments

    ########################################################

    def statefulsets(self):

        statefulsets = []

        response = self.apps.list_stateful_set_for_all_namespaces()

        for s in response.items:

            statefulsets.append(
                {
                    "namespace": s.metadata.namespace,
                    "name": s.metadata.name,
                    "replicas": s.spec.replicas or 0,
                }
            )

        return statefulsets

    ########################################################

    def daemonsets(self):

        daemonsets = []

        response = self.apps.list_daemon_set_for_all_namespaces()

        for d in response.items:

            daemonsets.append(
                {
                    "namespace": d.metadata.namespace,
                    "name": d.metadata.name,
                }
            )

        return daemonsets

    ########################################################

    def namespace_exists(self, namespace: str) -> bool:

        namespaces = self.namespaces()

        return any(ns.name == namespace for ns in namespaces)

    ########################################################

    def deployment_exists(self, namespace: str, deployment: str) -> bool:

        deployments = self.deployments()

        return any(
            d.namespace == namespace and d.name == deployment for d in deployments
        )
