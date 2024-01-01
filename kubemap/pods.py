from dataclasses import dataclass
from kubemap.config import get_config
from typing import List
import requests


config = get_config()


@dataclass
class Pod:
    ip: str
    name: str


class PodsException(Exception):
    pass


def get_pods(namespace) -> List[Pod]:
    headers = {
        "Authorization": f"Bearer {config.token}",
    }
    ls_pods_url = f"{config.server}/api/v1/namespaces/{namespace}/pods"
    response = requests.get(ls_pods_url, headers=headers, verify=False)
    if response.status_code == 200:
        return [
            Pod(
                ip=x.get("status", {}).get("podIP", None),
                name=x.get("metadata", {}).get("name", None)
            )
            for x in response.json().get("items", {})
            if x.get("metadata", {}).get("name", None) is not None
        ]
    raise PodsException(f"Error getting pods")
