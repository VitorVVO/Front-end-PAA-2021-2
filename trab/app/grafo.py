from django.urls import path
from pyvis.network import Network
import networkx as nx
import os

def inserircliente(grafo, cliente):
    grafo.add_node(cliente['id'], value=1, 
                    x = cliente['x'] * 200,
                    y = cliente['y'] * 200,
                    label='Cliente' + str(cliente['id']),
                    shape='image',
                    image='client.png',
                    )
    return grafo

def inserirvertice(grafo, vertice):
    if(vertice['type'] == 'Carro'):
        grafo.add_node(vertice['id'], value=1, 
                    x = vertice['x'] * 200,
                    y = vertice['y'] * 200,
                    label='Carro' + str(vertice['id']),
                    shape='image',
                    image='carro.png',
                    )

    elif(vertice['type'] == 'Normal'):
        grafo.add_node(vertice['id'], value=1, 
                    x = vertice['x'] * 200,
                    y = vertice['y'] * 200,
                    label='No' + str(vertice['id']),
                    shape ='dot',
                    color = '#FFFFFF'
                    )

    elif(vertice['type'] == 'Origem'):
        grafo.add_node("Origem", value=1, 
                    x = vertice['x'] * 200,
                    y = vertice['y'] * 200,
                    label=str("Origem"),
                    shape ='dot',
                    color = '#00FF00'
                    )

    elif(vertice['type'] == 'Destino'):
        grafo.add_node("Destino", value=1, 
                    x = vertice['x'] * 200,
                    y = vertice['y'] * 200,
                    label=str("Destino"),
                    shape ='dot',
                    color = '#ADD8E6',
                    )
    
    return grafo

def inserirarestas(grafo, arestas):
    for i in arestas:
        grafo.add_edge(i['from'], i['to'], color="#EE82EE")

    return grafo

def caminho(grafo, caminhos):
    # for i in range(0, len(c)-1):
    #     t = (c[i], c[i+1])
    #     cam_final.append(t)
    for i in caminhos:
        for j in grafo.edges:
            if(j['from'] == i[0] and j['to'] == i[1]):
                j['color'] = "#F7A156"
    
    return grafo

def c_grafo(caminho, cliente):
    if(caminho == 'grafo'):
        g = Network('700px', '900px', directed=True)
        g.toggle_drag_nodes(False)
        g.toggle_physics(False)

        aresta1 = {'from':1, 'to':2, 
                 'id': 1, 'veloc': 40, 
                 'weight' : 3.1 / 40 * 60, 
                 "distancia": 3.1}

        aresta2 = {'from':2, 'to':3, 
                 'id': 2, 'veloc': 35, 
                 'weight' : 2.6 / 35 * 60, 
                 "distancia": 2.6}

        aresta3 = {'from':3, 'to':1, 
                 'id': 3, 'veloc': 38, 
                 'weight' : 5.2 / 38 * 60, 
                 "distancia": 5.2}

        arestas = [aresta1, aresta2, aresta3]

        no1 = {'x': 2.2, 'y': 4.3, "type": 'Normal', 'id': 1}   

        no2 = {'x': 5.1, 'y': 3.2, "type": 'Normal', 'id': 2}

        no3 = {'x': 7.4, 'y': 4.4, "type": 'Normal', 'id': 3}

        carro1 = {'x': 7.4, 'y': 4.4, "type": 'Carro', 'id': 53}

        cliente1 = {'x': 5.0, 'y': 3.0, "type": 'Cliente', "id": 443}

        destino = {'x': 2.7, 'y': 4.1, "type": 'Destino'}

        nos = [no1, no2, no3, carro1, cliente1, destino]

        for i in nos:
            if(i["type"] == 'Cliente'):
                g = inserircliente(g, i)
            else:
                g = inserirvertice(g, i)

        g = inserirarestas(g, arestas)
        diretorio = (os.path.dirname(os.path.realpath(__file__)))
        dir =''
        for i in diretorio:
            if(i == '\\'):
                dir = dir + '/'
            else:
                dir = dir + i
        
        dir = dir + '/static/images/grafo.html' 

        g.save_graph(dir)

    else:
        g = Network('700px', '900px', directed=True)
        g.toggle_drag_nodes(False)
        g.toggle_physics(False)

        aresta1 = {'from':1, 'to':2, 
                 'id': 1, 'veloc': 40, 
                 'weight' : 3.1 / 40 * 60, 
                 "distancia": 3.1}

        aresta2 = {'from':2, 'to':3, 
                 'id': 2, 'veloc': 35, 
                 'weight' : 2.6 / 35 * 60, 
                 "distancia": 2.6}

        aresta3 = {'from':3, 'to':1, 
                 'id': 3, 'veloc': 38, 
                 'weight' : 5.2 / 38 * 60, 
                 "distancia": 5.2}

        arestas = [aresta1, aresta2, aresta3]

        no1 = {'x': 2.2, 'y': 4.3, "type": 'Normal', 'id': 1}   

        no2 = {'x': 5.1, 'y': 3.2, "type": 'Normal', 'id': 2}

        no3 = {'x': 7.4, 'y': 4.4, "type": 'Normal', 'id': 3}

        carro1 = {'x': 7.4, 'y': 4.4, "type": 'Carro', 'id': 53}

        cliente1 = {'x': 5.0, 'y': 3.0, "type": 'Cliente', "id": 443}

        destino = {'x': 2.7, 'y': 4.1, "type": 'Destino'}

        nos = [no1, no2, no3, carro1, cliente1, destino]

        for i in nos:
            if(i["type"] == 'Cliente'):
                g = inserircliente(g, i)
            else:
                g = inserirvertice(g, i)

        g = inserirarestas(g, arestas)
        diretorio = (os.path.dirname(os.path.realpath(__file__)))
        dir =''
        for i in diretorio:
            if(i == '\\'):
                dir = dir + '/'
            else:
                dir = dir + i
        
        dir = dir + '/static/images/c' + cliente + 'g' + caminho + '.html'

        g.save_graph(dir)

