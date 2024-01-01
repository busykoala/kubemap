from kubemap.config import get_config
import requests


config = get_config()


class NamespaceException(Exception):
    pass


def get_namespaces():
    headers = {
        "Authorization": f"Bearer {config.token}",
    }
    ls_ns_url = f"{config.server}/api/v1/namespaces"
    response = requests.get(ls_ns_url, headers=headers, verify=False)
    if response.status_code == 200:
        return [
            x.get("metadata", {}).get("name", None)
            for x in response.json().get("items", {})
            if x.get("metadata", {}).get("name", None) is not None
        ]
    raise NamespaceException("Failed to get namespaces")
