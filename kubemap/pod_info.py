from dataclasses import dataclass


@dataclass
class PodInfo:
    namespace: str
    pod_name: str
    pod_ip: str
    patch_container_name: str = ""
    logs: str = ""
    connections: list = None
