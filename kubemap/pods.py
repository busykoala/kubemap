from kubemap.config import get_config
import requests


config = get_config()


class PodsException(Exception):
    pass


def get_pods(namespace):
    headers = {
        "Authorization": f"Bearer {config.token}",
    }
    ls_pods_url = f"{config.server}/api/v1/namespaces/{namespace}/pods"
    response = requests.get(ls_pods_url, headers=headers, verify=False)
    if response.status_code == 200:
        return [
            x.get("metadata", {}).get("name", None)
            for x in response.json().get("items", {})
            if x.get("metadata", {}).get("name", None) is not None
        ]
    raise PodsException(f"Error getting pods")
