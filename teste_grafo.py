#essa pra fazer o grafo
from operator import length_hint
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

import pandas as pd

G = nx.Graph()

no1 = 'cliente1'
no2 = 'estacao1'
no3 = 'estacao2'
no4 = 'estacao3'
no5 = 'cliente2'

#lista com o nome de cada vertice
vertices = [no1, no2, no3, no4, no5]
# adicionando vertices
G.add_nodes_from(vertices)

#lista com as arestas e o peso das arestas
#(nó1, nó2, peso)
arestas = [(no1, no2, 5), (no2, no3, 10), (no3, no5, 4), (no3, no4, 15), (no4, no5, 2), (no2, no4, 7)]
G.add_weighted_edges_from(arestas)

#arestas do caminho que serao coloridas
arestas_caminho = [(no1, no2), (no2, no3), (no3, no5)]

#colorir apenas as arestas dos caminhos
list_no_origem = []
list_no_dest =  []
list_value = []

for aresta in G.edges:

    colorir = (aresta[0], aresta[1])
    list_no_origem.append(aresta[0])
    list_no_dest.append(aresta[1])

    if colorir in arestas_caminho:
        list_value.append('red')
    else:
        list_value.append('gray')

df = pd.DataFrame({'from':list_no_origem, 'to':list_no_dest, 'color':list_value})

#plotar grafo com os pesos escritos e cores

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, edge_color=df['color'], node_color = 'skyblue')
#nx.draw_networkx_edge_labels(G, pos)
plt.savefig("./trab/app/static/images/Graph.png", format="PNG")
#plt.show()
nt = Network("500px", "500px")
nt.from_nx(G)
for i in nt.edges:
    print(i)
    

nt.show_buttons()    
nt.show('alo.html')