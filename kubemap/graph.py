import matplotlib.pyplot as plt
import networkx as nx

def create_directed_graph(pod_connections):
    DG = nx.DiGraph()
    for pod, connections in pod_connections.items():
        for conn in connections:
            DG.add_edge(pod, conn)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(DG)  # Positions for all nodes
    nx.draw(
        DG,
        pos,
        with_labels=True,
        node_color='lightblue',
        node_size=2000,
        edge_color='gray',
        arrowstyle='-|>',
        arrowsize=12,
        linewidths=1,
        font_size=10
    )
    plt.savefig("graph.png")
