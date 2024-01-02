from kubemap.pod_info import PodInfo
import matplotlib.pyplot as plt
import networkx as nx
from typing import List


def calculate_bubble(ns_nodes, pos, padding=0.3):
    x_values, y_values = zip(*[pos[node] for node in ns_nodes])
    min_x, max_x = min(x_values), max(x_values)
    min_y, max_y = min(y_values), max(y_values)
    center = ((min_x + max_x) / 2, (min_y + max_y) / 2)
    radius = max(max_x - min_x, max_y - min_y) / 2 + padding
    return center, radius


def create_directed_graph(pod_info: List[PodInfo]):
    G = nx.DiGraph()
    for pod in pod_info:
        G.add_node(pod.pod_name, ns=pod.namespace)
        for connection in pod.connections:
            G.add_edge(pod.pod_name, connection)
    pos = nx.spring_layout(G, k=3, iterations=50)
    namespace_offset = {
        ns: i * 3 for i, ns
        in enumerate(set(pod.namespace for pod in pod_info))
    }
    for node in G.nodes():
        ns = G.nodes[node]['ns']
        pos[node] = (pos[node][0] + namespace_offset[ns], pos[node][1])
    plt.figure(figsize=(20, 15))
    for ns in set(pod.namespace for pod in pod_info):
        ns_nodes = [pod.pod_name for pod in pod_info if pod.namespace == ns]
        color = plt.cm.jet(0.5 + 0.5 * hash(ns) / 2**64)
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=ns_nodes,
            node_color=[color for _ in ns_nodes],
            label=ns,
            node_size=200,
        )
        center, radius = calculate_bubble(ns_nodes, pos)
        ellipse = plt.Circle(
            center,
            radius,
            color=color,
            fill=False,
            linestyle='--',
            linewidth=2
        )
        plt.gca().add_patch(ellipse)
    nx.draw_networkx_edges(
        G, pos, arrowstyle='->', arrowsize=20,
        connectionstyle='arc3, rad=0.1',
        edge_color='lightskyblue',
    )
    for node, (x, y) in pos.items():
        plt.text(x, y, node, fontsize=10, ha='right', va='center')
    plt.xlim(min(x for x, y in pos.values()) - 1, max(x for x, y in pos.values()) + 1)
    plt.ylim(min(y for x, y in pos.values()) - 1, max(y for x, y in pos.values()) + 1)
    plt.legend(scatterpoints=1)
    plt.title("Pod network connections by namespace", fontsize=15, fontweight='bold')
    plt.axis('off')
    plt.savefig("graph.png", bbox_inches='tight')
