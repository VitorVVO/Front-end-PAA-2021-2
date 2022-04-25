from django.urls import path
from pyvis.network import Network
import networkx as nx
import os
from .p import *
from .algoritmo import *

def inserircliente(grafo, cliente, ex):
    if(ex == 0):
        grafo.add_node(cliente[0], value=1, 
                        x = cliente[1]['x'] * 200,
                        y = cliente[1]['y'] * -200,
                        label='Cliente' + str(cliente[1]['type_id']),
                        shape='image',
                        image='client.png',
                        )
    else:
        grafo.add_node(cliente[0], value=1, 
                        x = cliente[1]['x'] * 200,
                        y = cliente[1]['y'] * -200,
                        label='Cliente' + str(cliente[1]['type_id']),
                        shape='image',
                        image='client.png',
                        )
    return grafo

def inserirvertice(grafo, vertice, ex):
    if(vertice[1]['type'] == 'carro'):
        grafo.add_node(vertice[0], value=0.90, 
                    x = vertice[1]['x'] * 200,
                    y = vertice[1]['y'] * -200,
                    label='Carro' + str(vertice[1]['type_id']),
                    shape='image',
                    image='carro_2.png',
                    )
    elif(vertice[1]['type'] == None):
        grafo.add_node(vertice[0], value=0.8, 
                    x = vertice[1]['x'] * 200,
                    y = vertice[1]['y'] * -200,
                    label='No' + str(vertice[0]),
                    shape ='dot',
                    color = '#000000',
                    )

    elif(vertice[1]['type'] == 'partida' and ex == 1):
        grafo.add_node(vertice[0], value=0.8, 
                    x = vertice[1]['x'] * 200,
                    y = vertice[1]['y'] * -200,
                    label=str("Partida" + str(vertice[1]['type_id'])),
                    shape ='star',
                    color = '#f7ff00'
                    )
    
    elif(vertice[1]['type'] == 'destino' and ex == 1):
        grafo.add_node(vertice[0], value=0.8, 
                    x = vertice[1]['x'] * 200,
                    y = vertice[1]['y'] * -200,
                    label=str("Destino" + str(vertice[1]['type_id'])),
                    shape ='star',
                    color = '#FF0000',
                    )

    elif(vertice[1]['type'] == 'partida' and ex == 0):
        grafo.add_node(vertice[0], value=0.8, 
                    x = vertice[1]['x'] * 200,
                    y = vertice[1]['y'] * -200,
                    hidden = True,
                    )

    elif(vertice[1]['type'] == 'destino' and ex == 0):
        grafo.add_node(vertice[0], value=0.8, 
                    x = vertice[1]['x'] * 200,
                    y = vertice[1]['y'] * -200,
                    hidden = True,
                    )
    
    return grafo

def inserircarro_c(grafo, vertice):
    grafo.add_node(vertice[0], value=0.85, 
                    x = vertice[1]['x'] * 200,
                    y = vertice[1]['y'] * -200,
                    label='Carro' + str(vertice[1]['type_id']),
                    shape='image',
                    image='carro.png',
                    )
    return grafo

def inserirarestas(grafo, arestas):
    for i in arestas:
        grafo.add_edge(i[0], i[1], color = "#000000")

    return grafo

def caminho(grafo, caminhos):
    cam_final = []
    for i in range(0, len(caminhos)-1):
        t = (caminhos[i], caminhos[i+1])
        cam_final.append(t)

    for i in cam_final:
        for j in grafo.edges:
            if(j['from'] == i[0] and j['to'] == i[1]):
                j['color'] = "#F7A156"
    
    return grafo

def c_grafo(caminhoid, cliente, grafo, lista_carros, lista_clientes):
    if(caminhoid == '0' and cliente == '0'):
        g = Network('700px', '900px', directed=True)
        g.toggle_drag_nodes(False)
        g.toggle_physics(False)

        nos = grafo.nodes(data=True)
        arestas = grafo.edges(data=True)

        for i in nos:
            if(i[1]['type'] == 'cliente'):
                g = inserircliente(g, i, 0)
            else:
                g = inserirvertice(g, i, 1)

        g = inserirarestas(g, arestas)
        diretorio = (os.path.dirname(os.path.realpath(__file__)))
        dir =''
        for i in diretorio:
            if(i == '\\'):
                dir = dir + '/'
            else:
                dir = dir + i
        
        dir = dir + '/static/images/c0g0.html' 

        g.save_graph(dir)

        tempo = 0

        return tempo
    else:
        g = Network('700px', '900px', directed=True)
        g.toggle_drag_nodes(True)
        g.toggle_physics(False)

        nos = grafo.nodes(data=True)
        arestas = grafo.edges(data=True)
        partida, destino = 0,0
        a = get_node_carro(grafo, int(cliente), lista_carros, lista_clientes)
        for i in nos:     
            if(i[1]['type'] == 'cliente' and i[1]['type_id'] == int(cliente)):
                g = inserircliente(g, i, 1)
            else:
                if(i[1]['type'] == 'partida' and i[1]['type_id'] == int(cliente)):
                    partida = i[0]
                    g = inserirvertice(g, i, 1)
                elif(i[1]['type'] == 'destino' and i[1]['type_id'] == int(cliente)):
                    destino = i[0]
                    g = inserirvertice(g, i, 1)
                elif(i[1]['type'] == 'carro' and i[1]['type_id'] == a):
                    g = inserircarro_c(g, i)
                else:
                    g = inserirvertice(g, i, 0)


        g = inserirarestas(g, arestas)
        
        caminhos, tempo = caminhos_mais_curtos(grafo, partida, destino, k=5, weight='weight')
        
        g = caminho(g, caminhos[int(caminhoid)-1])
        
        
        diretorio = (os.path.dirname(os.path.realpath(__file__)))
        dir =''
        for i in diretorio:
            if(i == '\\'):
                dir = dir + '/'
            else:
                dir = dir + i
        
        dir = dir + '/static/images/c' + cliente + 'g' + caminhoid + '.html' 

        g.save_graph(dir)

        return tempo[int(caminhoid)-1]