import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

#lista com o nome de cada vertice
vertices = [1, 2, 3]
# adicionando vertices
G.add_nodes_from(vertices)

#lista com as arestas e o peso das arestas
#(nó1, nó2, peso)
arestas = [(1, 2, 10), (1, 3, 1), (2, 3, 4)]
G.add_weighted_edges_from(arestas)

#plotar grafo com os pesos escritos
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos)
plt.show()