from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from kubemap.logs import get_logs
from kubemap.namespaces import get_namespaces
from kubemap.patch import PatchException
from kubemap.patch import patch_pod
from kubemap.pods import get_pods
import click
import time


@dataclass
class PodInfo:
    namespace: str
    pod_name: str
    patch_container_name: str = ""
    logs: str = ""


def process_pod(pod):
    try:
        pod.patch_container_name = patch_pod(pod.namespace, pod.pod_name)
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
                    pod_name=pod
                )
            )

    print("Patching pods")
    with ThreadPoolExecutor(max_workers=len(pod_info)) as executor:
        executor.map(process_pod, pod_info)

    print("Waiting for pods to be ready")
    time.sleep(20)

    print("Getting logs")
    with ThreadPoolExecutor(max_workers=len(pod_info)) as executor:
        executor.map(get_pod_logs, pod_info)

    for result in pod_info:
        print(result)


if __name__ == '__main__':
    cli()
