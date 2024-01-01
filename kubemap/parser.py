from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Connection:
    pod_name: str
    port: str


def parse_logs(log: str, pod_info) -> List[Connection]:
    log_entries = log.strip().split('\n')
    connections = []
    for entry in log_entries:
        if 'Connection to' in entry and 'succeeded' in entry:
            parts = entry.split()
            address = parts[2]
            ip, port = address.split(':')
            matching_pod_info = next((p for p in pod_info if p.pod_ip == ip), None)
            if matching_pod_info is not None:
                connections.append(
                    Connection(
                        pod_name=matching_pod_info.pod_name,
                        port=port
                    )
                )
    return connections
