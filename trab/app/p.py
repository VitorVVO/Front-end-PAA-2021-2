import networkx as nx
import copy as cp

def backtrace(pai, start, end):
    caminho = [end]
    while caminho[-1] != start:
        caminho.append(pai[caminho[-1]])
    caminho.reverse()
    return caminho

def dijkstra(grafo_in: nx.DiGraph, origem, destino=None, weight='weight'):

    fila = []
    visitado = {}
    distancia = {}
    menor_distancia = {}
    pai = {}
    caminho = []

    for node in grafo_in.nodes:
        distancia[node] = None
        visitado[node] = False
        pai[node] = None
        menor_distancia[node] = float("inf")

    fila.append(origem)
    distancia[origem] = 0
    while len(fila) != 0:
        corrente = fila.pop(0)
        visitado[corrente] = True
        if corrente == destino:
            caminho = backtrace(pai, origem, destino)
        for neighbor in grafo_in.successors(corrente):
            if visitado[neighbor] == False:
                distancia[neighbor] = distancia[corrente] + grafo_in[corrente][neighbor]['weight']

                if distancia[neighbor] < menor_distancia[neighbor]:
                    menor_distancia[neighbor] = distancia[neighbor]
                    pai[neighbor] = corrente
                    fila.append(neighbor)
    if destino == None:
        # Se for assim, calcula o caminho usando backtrace
        return (pai)
    else:
        return (caminho)


def caminhos_mais_curtos(G, origem, destino, k=1, weight='weight'):
    A = [dijkstra(G, origem, destino)]
    A_peso = [sum([G[A[0][l]][A[0][l + 1]]['weight'] for l in range(len(A[0]) - 1)])]
    B = []

    for i in range(1, k):
        for j in range(0, len(A[-1]) - 1):
            Gcopy = cp.deepcopy(G)
            no_expurgo = A[-1][j]
            caminho_raiz = A[-1][:j + 1]
            for caminho in A:
                if caminho_raiz == caminho[0:j + 1] and len(caminho) > j:
                    if Gcopy.has_edge(caminho[j], caminho[j + 1]):
                        Gcopy.remove_edge(caminho[j], caminho[j + 1])
                    if Gcopy.has_edge(caminho[j + 1], caminho[j]):
                        Gcopy.remove_edge(caminho[j + 1], caminho[j])
            for n in caminho_raiz:
                if n != no_expurgo:
                    Gcopy.remove_node(n)
            caminho_expurgo = dijkstra(Gcopy, no_expurgo, destino)
            if len(caminho_expurgo) == 0:
                continue
            else:
                caminho_total = caminho_raiz + caminho_expurgo[1:]
                if caminho_total not in B:
                    B += [caminho_total]
        if len(B) == 0:
            break
        B_peso = [sum([G[caminho[l]][caminho[l + 1]]['weight'] for l in range(len(caminho) - 1)]) for caminho in B]
        B = [p for _, p in sorted(zip(B_peso, B))]
        A.append(B[0])
        A_peso.append(sorted(B_peso)[0])
        B.remove(B[0])
    return A, A_peso