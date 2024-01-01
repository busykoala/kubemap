import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as patches


def create_directed_graph(pod_connections, pod_info):
    # Create a directed graph from the connections data
    DG = nx.DiGraph()
    for pod, connections in pod_connections.items():
        for conn in connections:
            DG.add_edge(pod, conn)

    # Layout
    pos = nx.spring_layout(DG)

    # Set margins for the plot
    plt.figure(figsize=(15, 10))
    plt.margins(0.1)

    # Draw the graph
    nx.draw(DG, pos, with_labels=True, node_color='lightblue', node_size=3000, edge_color='gray', arrowstyle='-|>', arrowsize=15, font_size=12)

    # Group nodes by namespace and draw boxes
    namespaces = {pod.namespace: [] for pod in pod_info}
    for pod in pod_info:
        namespaces[pod.namespace].append(pod.pod_name)

    for namespace, nodes in namespaces.items():
        node_positions = [pos[node] for node in nodes if node in pos]
        if not node_positions:  # skip if no positions (no nodes)
            continue

        xs, ys = zip(*node_positions)
        min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
        width, height = max_x - min_x + 0.2, max_y - min_y + 0.2
        rect = patches.Rectangle((min_x - 0.1, min_y - 0.1), width, height, linewidth=2, edgecolor='black', facecolor='none')
        plt.gca().add_patch(rect)
        plt.text(min_x, max_y + 0.1, namespace, horizontalalignment='left', size='medium', color='black', weight='semibold')

    # Adjust layout to fit all labels and boxes
    plt.tight_layout()

    # Save and show the plot
    plt.savefig('graph.png')
