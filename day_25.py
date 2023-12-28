
import networkx as nx, math

graph = nx.Graph()

for line in open('day_25_input.txt'):
    source, targets = line.split(':')
    stripped_source = source.strip()
    for target in targets.split(' '):
        if target != '':
            graph.add_edge(source, target.strip())


shortest_paths = nx.all_pairs_shortest_path(graph)
path_lengths = {node:[] for node in graph.nodes}
for from_node, paths in shortest_paths:
    lengths = []
    for to_node in paths:
        lengths.append(len(paths[to_node]))
    path_lengths[from_node] = sum(lengths) / len(lengths)
top_nodes = sorted(path_lengths.items(), key=lambda item: item[1])[:6]
print(top_nodes)
sub_graph = graph.subgraph([node for (node, avg) in top_nodes])

for edge1 in sub_graph.edges():
    for edge2 in sub_graph.edges():
        for edge3 in sub_graph.edges():
            if edge1 != edge2 and edge1 != edge3 and edge2 != edge3:
                test_graph = nx.Graph(graph)
                test_graph.remove_edge(*edge1)
                test_graph.remove_edge(*edge2)
                test_graph.remove_edge(*edge3)
                subs = [len(sub) for sub in nx.connected_components(test_graph)]
                if len(subs) > 1:
                    print('edges to remove are:', edge1, edge2, edge3)
                    print('product of subgraph sizes is', subs[0] * subs[1])
                    exit()