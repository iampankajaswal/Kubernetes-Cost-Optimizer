import typer
from rich.console import Console
from rich.table import Table

from k8s_cost_optimizer.config import Config
from k8s_cost_optimizer.clients.kubernetes import KubernetesClient

app = typer.Typer(help="Kubernetes Cost Optimizer")
console = Console()

config = Config()
k8s = KubernetesClient()


@app.command()
def version():
    """Show application version."""
    console.print("[bold green]Kubernetes Cost Optimizer[/bold green]")
    console.print("Version: 0.1.0")


@app.command("show-config")
def show_config():
    """Display loaded configuration."""
    console.print(config.data)


@app.command()
def scan():
    """Discover Kubernetes resources."""

    console.print("\n[bold green]Connecting to Kubernetes...[/bold green]")

    try:
        k8s.connect()
        console.print("[green]✓ Connected[/green]\n")
    except Exception as e:
        console.print("[bold red]✗ Unable to connect to Kubernetes[/bold red]")
        console.print(f"[yellow]{e}[/yellow]")
        raise typer.Exit(code=1)

    namespaces = k8s.namespaces()
    nodes = k8s.nodes()
    deployments = k8s.deployments()
    statefulsets = k8s.statefulsets()
    daemonsets = k8s.daemonsets()
    pods = k8s.pods()

    summary = Table(title="Cluster Summary")

    summary.add_column("Resource", style="cyan")
    summary.add_column("Count", justify="right", style="green")

    summary.add_row("Namespaces", str(len(namespaces)))
    summary.add_row("Nodes", str(len(nodes)))
    summary.add_row("Deployments", str(len(deployments)))
    summary.add_row("StatefulSets", str(len(statefulsets)))
    summary.add_row("DaemonSets", str(len(daemonsets)))
    summary.add_row("Pods", str(len(pods)))

    console.print(summary)

    console.print("\n[bold]Namespaces[/bold]")

    namespace_table = Table()

    namespace_table.add_column("Name", style="cyan")
    namespace_table.add_column("Status", style="green")

    for ns in namespaces:
        namespace_table.add_row(
            ns.name,
            ns.status,
        )

    console.print(namespace_table)

    console.print("\n[green]✓ Cluster discovery completed successfully.[/green]")


@app.command()
def nodes():
    """List Kubernetes nodes."""

    k8s.connect()

    table = Table(title="Nodes")

    table.add_column("Name")
    table.add_column("OS")
    table.add_column("Kernel")
    table.add_column("Kubelet")

    for node in k8s.nodes():
        table.add_row(
            node["name"],
            node["os"],
            node["kernel"],
            node["kubelet"],
        )

    console.print(table)


@app.command()
def deployments():
    """List Kubernetes deployments."""

    k8s.connect()

    table = Table(title="Deployments")

    table.add_column("Namespace")
    table.add_column("Deployment")
    table.add_column("Replicas", justify="right")

    for deployment in k8s.deployments():
        table.add_row(
            deployment.namespace,
            deployment.name,
            str(deployment.replicas),
        )

    console.print(table)


@app.command()
def pods():
    """List Kubernetes pods."""

    k8s.connect()

    table = Table(title="Pods")

    table.add_column("Namespace")
    table.add_column("Pod")
    table.add_column("Status")
    table.add_column("Node")

    for pod in k8s.pods():
        table.add_row(
            pod["namespace"],
            pod["name"],
            pod["status"],
            pod["node"] if pod["node"] else "-",
        )

    console.print(table)


if __name__ == "__main__":
    app()
