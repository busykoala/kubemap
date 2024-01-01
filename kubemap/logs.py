from kubemap.config import get_config
import requests


config = get_config()


class LogsException(Exception):
    pass


def get_logs(namespace, pod_name, container_name):
    headers = {
        "Authorization": f"Bearer {config.token}",
    }
    logs_url = f"{config.server}/api/v1/namespaces/{namespace}/pods/{pod_name}/log?container={container_name}"
    response = requests.get(logs_url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.text
    raise LogsException("Failed to get logs")
