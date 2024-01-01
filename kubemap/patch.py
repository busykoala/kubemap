from kubemap.config import get_config
import requests
import uuid

config = get_config()

class PatchException(Exception):
    pass


def patch_pod(namespace: str, pod_name: str, pod_ips: str) -> str:
    container_name = f"kubemap-{uuid.uuid4()}"
    image_name = "ghcr.io/busykoala/kubemap:main"

    patch_url = f"{config.server}/api/v1/namespaces/{namespace}/pods/{pod_name}/ephemeralcontainers"
    patch_data = {
        "spec": {
            "ephemeralContainers": [
                {
                    "name": container_name,
                    "image": image_name,
                    "command": [
                        f"/multiport-listener {pod_ips}"
                    ],
                    "stdin": True,
                    "terminationMessagePolicy": "File",
                    "tty": True
                }
            ]
        }
    }
    headers = {
        "Authorization": f"Bearer {config.token}",
        "Content-Type": "application/strategic-merge-patch+json"
    }
    response = requests.patch(patch_url, json=patch_data, headers=headers, verify=False)
    if response.status_code == 200:
        return container_name
    raise PatchException("Failed to patch pod")
