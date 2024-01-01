from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial
from kubemap.logs import get_logs
from kubemap.namespaces import get_namespaces
from kubemap.patch import PatchException
from kubemap.patch import patch_pod
from kubemap.pods import get_pods
from kubemap.parser import parse_logs
from kubemap.graph import create_directed_graph
import click
import time


@dataclass
class PodInfo:
    namespace: str
    pod_name: str
    pod_ip: str
    patch_container_name: str = ""
    logs: str = ""


def process_pod(pod: PodInfo, pod_ips: str):
    try:
        pod.patch_container_name = patch_pod(pod.namespace, pod.pod_name, pod_ips)
    except PatchException:
        pod.logs = "patch failed"


def get_pod_logs(pod):
    if pod.patch_container_name != "":
        pod.logs = get_logs(pod.namespace, pod.pod_name, pod.patch_container_name)


@click.command()
def cli():
    """Patch a pod and get logs"""

    namespaces = get_namespaces()

    pod_info = []
    for namespace in namespaces:
        ns_pods = get_pods(namespace)
        for pod in ns_pods:
            pod_info.append(
                PodInfo(
                    namespace=namespace,
                    pod_ip=pod.ip,
                    pod_name=pod.name
                )
            )
    pod_ips = ';'.join([pod.pod_ip for pod in pod_info])

    print("Patching pods")
    with ThreadPoolExecutor(max_workers=len(pod_info)) as executor:
        func = partial(process_pod, pod_ips=pod_ips)
        executor.map(func, pod_info)

    print("Waiting for pods to be ready")
    time.sleep(50)

    print("Getting logs")
    with ThreadPoolExecutor(max_workers=len(pod_info)) as executor:
        executor.map(get_pod_logs, pod_info)

    pod_connections = {}
    for pod in pod_info:
        connections = [x for x in set(parse_logs(pod.logs, pod_info))
                       if x.pod_name != pod.pod_name]
        pod_connections[pod.pod_name] = [x.pod_name for x in connections]
    create_directed_graph(pod_connections)


if __name__ == '__main__':
    cli()
