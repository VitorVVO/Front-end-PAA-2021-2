import networkx as nx
# import pandas as pd
import matplotlib.pyplot as plt
from queue import PriorityQueue
from math import inf

# tabela = pd.read_csv("paa_arquivo_proj_grafo.txt", delimiter=" ")
# tabela['tempo_minutos'] = (tabela['Distância_km'] / tabela['Velocidade_km_h']) * 60
# pd.set_option('display.max_columns', 10)
# print(tabela)


# grafo = nx.from_pandas_edgelist(tabela, source="v_origem", target="v_destino", edge_key="Aresta_n", edge_attr=True)
# nx.draw_networkx(grafo, with_labels=True)
# plt.show()

def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path

# print (range(len(grafo)-1))

def dijkstra(graph: nx.DiGraph, source, target = None):
    queue = []
    visited = {}
    distance = {}
    shortest_distance = {}
    parent = {}

    for node in range(1, len(graph)+1):
        distance[node] = None
        visited[node] = False
        parent[node] = None
        shortest_distance[node] = float("inf")

    queue.append(source)
    distance[source] = 0
    while len(queue) != 0:
        current = queue.pop(0)
        visited[current] = True
        if current == target:
            caminho = backtrace(parent, source, target)
        
            # break
        for neighbor in graph.successors(current):
            if visited[neighbor] == False:
                # print(graph[current, neighbor])
                # distance[neighbor] = distance[current] + 1
                distance[neighbor] = distance[current] + graph[current][neighbor]['weight']

                if distance[neighbor] < shortest_distance[neighbor]:
                    shortest_distance[neighbor] = distance[neighbor]
                    parent[neighbor] = current
                    queue.append(neighbor)


    # print(caminho)
    # print("distancia:",  distance)
    # print("menor d", shortest_distance)
    # print("parent", parent)
    # print("target", target)
    # return 
    if target == None:
        return (distance, shortest_distance, parent) # Se for assim, calcula o caminho usando backtrace
        
    else:
        return (distance, shortest_distance, caminho)

# dijkstra(grafo,1,6)
# nx.draw(grafo)
# nx.draw_networkx(grafo, with_labels=True)
# plt.show()