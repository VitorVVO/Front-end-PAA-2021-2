from .models import Carro
from .models import Cliente
from .models import Grafo
from .p import *
from .calc_dist import calcula_km_nos

import networkx as nx
from math import sqrt, ceil

class Cliente_info:

    def __init__(self, id: int, ponto_loc, ponto_dest) -> None:
        self.id = id
        self.loc_x,  self.loc_y  = ponto_loc
        self.dest_x, self.dest_y = ponto_dest

        self.p1 = self.p2 = None # Pra guardar o ponto (nodes) de localizacao e destino que ele quer ir

        # Pra guardar o ponto na aresta onde o cliente vai pegar/chegar na viagem, junto com a distancia
        # (x, y, distancia)
        self.p_local = ()
        self.p_destino = ()
        self.node_dest = self.node_loc = None # Nos de destino e localizacao calculados pra pegar carro

    def get_loc(self):
        return (self.loc_x, self.loc_y)

    def get_dest(self):
        return (self.dest_x, self.dest_y)

    def __str__(self):
        return f"""Cliente {self.id} {"" if self.p1 == None else f"em {self.p1}"}"""
        # return f"Cliente {self.id} -> loc = {self.aresta_local}, dest = {self.aresta_destino}"        
        return f"Cliente {self.id} -> loc = {self.get_loc()}, dest = {self.get_dest()}"

    def __repr__(self) -> str:
        # return f"Cliente {self.id} p {self.my_node} d {self.no_destino}"
        return self.__str__()

class Carro_info:

    def __init__(self, id, ponto_loc, aresta_id) -> None:
        self.loc_x, self.loc_y = ponto_loc
        self.id = id
        self.aresta_id = aresta_id

        self.my_node = None # O no onde o carro se encontra

        # self.aresta_local = ()


    def get_loc(self):
        return (self.loc_x, self.loc_y)

    def __str__(self):
        return f"""Carro {self.id} {"" if self.my_node == None else f"em {self.my_node}"}"""

    def __repr__(self) -> str:
        # return f"Carro {self.id} p {self.aresta_local}"
        return self.__str__()

def make_graph():

    arestas = Grafo.objects.all()

    lista_arestas = []
    attr_nos = dict()

    for a in arestas:
        # a_temp = (a.v_origem, a.v_destino, {'id': a.aresta_n, 'veloc': a.velocidade_km_h, 'weight' : a.distancia_km / a.velocidade_km_h * 60, "tem_carro" : False, 
        # "cliente_partida" : dict(), "cliente_destino" : dict(), "lista_carros": dict()}) # <- Lista de carros e clientes

        # Dados dos vertices
        # attr_nos[a.v_origem] = {'x': a.loc_v_origem_x, 'y' : a.loc_v_origem_y}
        # attr_nos[a.v_destino] = {'x': a.loc_v_destino_x, 'y' : a.loc_v_destino_y}


        a_temp = (a.v_origem, a.v_destino, {'id': a.aresta_n, 'veloc': a.velocidade_km_h, 'weight' : a.distancia_km / a.velocidade_km_h * 60, 
        "distancia": a.distancia_km})
        lista_arestas.append(a_temp)

        attr_nos[a.v_origem] = {'x': a.loc_v_origem_x, 'y' : a.loc_v_origem_y, 
        "type": None, 'type_id' : None}
        attr_nos[a.v_destino] = {'x': a.loc_v_destino_x, 'y' : a.loc_v_destino_y, 
        "type": None, 'type_id' : None}


    Mapa = nx.DiGraph()
    Mapa.add_edges_from(lista_arestas)
    nx.set_node_attributes(Mapa, attr_nos)

    return Mapa

def obter_ponto_cliente(p_cliente, p_1, p_2):
# def obter_ponto_cliente(x : int, y:int, x1:int, y1:int, x2:int, y2:int):
    # Obtem o ponto mais proximo do cliente em uma linha

    x, y = p_cliente
    x1, y1 = p_1
    x2, y2 = p_2

    A = x - x1
    B = y - y1
    C = x2 - x1
    D = y2 - y1

    dot    = A * C + B * D
    len_sq = C * C + D * D
    param  = -1

    if len_sq != 0: # Se a linha tem tamanho 0, entao ponto1 == ponto2, o resultado sera a distancia do ponto 1
        param = dot / len_sq

    x_cliente = y_cliente = 0 # Declarando variaveis

    if param < 0:
        x_cliente = x1
        y_cliente = y1

    elif param > 1:
        x_cliente = x2
        y_cliente = y2

    else:
        x_cliente = x1 + param * C
        y_cliente = y1 + param * D

    dx = x - x_cliente
    dy = y - y_cliente
    
    dist = sqrt(dx * dx + dy * dy)

    return (x_cliente, y_cliente, dist)
        
def marcar_ponto_cliente(cl: Cliente_info, mapa: nx.DiGraph, qual = "loc"):
    """ Retorna o ponto na aresta mais proximo do cliente. Use a varivavel qual para indicar se eh localizacao 
    ou destino. Se qual == loc, usa a loc, se nao o destino eh usado. Retorna uma tupla na forma (aresta_id, (x, y, dist)), 
    em que aresta_id eh o id da aresta, x e y, a localizacao, dist e a distancia minima """

    if qual == "loc":
        point = cl.get_loc()
    else:
        point = cl.get_dest()

    partida_cliente = point
    partida_cliente = (partida_cliente[0], partida_cliente[1], 10**100)
    aresta_partida = -1 # Contem o id da aresta em que o ponto sera marcado

    # print(qual, cl)

    for aresta in mapa.edges(data=True):
        p1 = (mapa.nodes[aresta[0]]['x'], mapa.nodes[aresta[0]]['y'])
        p2 = (mapa.nodes[aresta[1]]['x'], mapa.nodes[aresta[1]]['y'])

        temp = obter_ponto_cliente(point, p1, p2)

        # print(temp, aresta[2]['id'])
        if temp[-1] < partida_cliente[-1]:
            partida_cliente = temp
            aresta_partida = aresta[2]['id']

    return (aresta_partida, partida_cliente)
        
def get_clientes():

    clientes_query = Cliente.objects.all()

    clientes = []

    for q in clientes_query:

        loc = (q.loc_cliente_x, q.loc_cliente_y)
        dest = (q.dest_cliente_x, q.dest_cliente_y)
        novo_cliente = Cliente_info(id = q.cliente_id, ponto_loc=loc, ponto_dest=dest)

        clientes.append(novo_cliente)

    
    return clientes

def get_carros():

    carros_query = Carro.objects.all()

    carros = []

    for q in carros_query:
        loc = (q.loc_carro_x, q.loc_carro_y)
        novo_carro = Carro_info(id= q.carro_id, ponto_loc= loc, aresta_id= q.aresta_id)

        carros.append(novo_carro)

    return carros

def get_aresta_ids(mapa: nx.DiGraph):
    """ Retorna o identificadores de aresta, isto e', uma tupla com vertices daquela aresta. """
    temp = nx.get_edge_attributes(mapa, 'id')
    temp = dict(zip(temp.values(), temp.keys()))

    return temp

def get_novo_node_num(mapa: nx.DiGraph):
    """ Retorna um numero para um novo no """

    lista_nos = sorted(list(mapa.nodes))
    novo_no_id: int = lista_nos[-1] + 1

    return novo_no_id

def marcar_carros(mapa: nx.DiGraph):
    """ Retorna o mapa e uma lista de carros, com os dados de cada carro """

    carros = get_carros()

    lista_carros = []
    for car in carros:
        aresta_cd = get_aresta_ids(mapa)

        novo_no_id = get_novo_node_num(mapa)

        # Os vertices de inicio e fim da aresta
        init = aresta_cd[car.aresta_id][0]
        end = aresta_cd[car.aresta_id][1]

        car.my_node = novo_no_id        
        aresta_attr = mapa.get_edge_data(init, end)

        # Copiando atributos das novas arestas
        n1_aresta_att: dict = aresta_attr.copy()
        n2_aresta_att: dict = aresta_attr.copy()

        # Calculando distancias
        d1, d2 = calcula_km_nos(km_aresta=aresta_attr["distancia"], 
        x_aresta1=mapa.nodes[init]['x'], y_aresta1=mapa.nodes[init]['y'],
        x_aresta2=mapa.nodes[end]['x'], y_aresta2=mapa.nodes[end]['y'], 
        x_embarque1=car.loc_x, y_embarque1=car.loc_y)

        n1_aresta_att["distancia"] = d1
        n2_aresta_att["distancia"] = d2

        # Calculando pesos
        n1_aresta_att["weight"] = d1 / n1_aresta_att['veloc'] * 60
        n2_aresta_att['weight'] = d2 / n2_aresta_att['veloc'] * 60

        # Obtendo dados do novo node
        node_att = {'x': car.loc_x, 'y': car.loc_y, 'type': 'carro', 'type_id': car.id}

        # Atualizando o grafo
        mapa.remove_edge(init, end)

        mapa.add_node(novo_no_id)
        mapa.nodes[novo_no_id].update(node_att)

        mapa.add_edge(init, novo_no_id)
        mapa.edges[init, novo_no_id].update(n1_aresta_att)
        
        mapa.add_edge(novo_no_id, end)
        mapa.edges[novo_no_id, end].update(n2_aresta_att)

        lista_carros.append(car)

    return (mapa, lista_carros)

def add_novo_node(mapa: nx.DiGraph, aresta: tuple, novo_node_num: int, node_att: dict, a1_att: dict, a2_att: dict):
        
    init, end = aresta    
    mapa.remove_edge(*aresta)

    mapa.add_node(novo_node_num)
    mapa.nodes[novo_node_num].update(node_att)

    mapa.add_edge(init, novo_node_num)
    mapa.edges[init, novo_node_num].update(a1_att)
    
    mapa.add_edge(novo_node_num, end)
    mapa.edges[novo_node_num, end].update(a2_att)

    return mapa

def split_attributes(mapa: nx.DiGraph, aresta: tuple, x: float, y: float):
    """ Pega o atributo da aresta e divide em dois """
    init, end = aresta
    aresta_attr = mapa.get_edge_data(init, end)

    # Copiando atributos das novas arestas
    n1_aresta_att: dict = aresta_attr.copy()
    n2_aresta_att: dict = aresta_attr.copy()

    # Calculando distancias
    d1, d2 = calcula_km_nos(km_aresta=aresta_attr["distancia"], 
    x_aresta1=mapa.nodes[init]['x'], y_aresta1=mapa.nodes[init]['y'],
    x_aresta2=mapa.nodes[end]['x'], y_aresta2=mapa.nodes[end]['y'], 
    x_embarque1=x, y_embarque1=y)

    n1_aresta_att["distancia"] = d1
    n2_aresta_att["distancia"] = d2

    # Calculando pesos
    n1_aresta_att["weight"] = d1 / n1_aresta_att['veloc'] * 60
    n2_aresta_att['weight'] = d2 / n2_aresta_att['veloc'] * 60

    return n1_aresta_att, n2_aresta_att

def marcar_clientes(mapa: nx.DiGraph):
    """ Marca as informacoes do cliente no mapa. Marca a sua localizacao e seu destino no mapa, indicando 
    em uma aresta tais dados. """

    clientes = get_clientes()

    lista_clientes = []
    for c in clientes:
        # Marcando o ponto de partida 
        # p_localizacao = marcar_ponto_cliente(c, mapa, qual = 'loc')
        # aresta_idx = get_aresta(p_localizacao[0], mapa)
        # mapa.edges[ aresta_idx[0], aresta_idx[1] ]['cliente_partida'][c.id] = (c, p_localizacao)

        # Marcando o ponto de destino
        # p_destino = marcar_ponto_cliente(c, mapa, qual = 'dest')
        # aresta_idx = get_aresta(p_destino[0], mapa)
        # mapa.edges[ aresta_idx[0], aresta_idx[1] ]['cliente_destino'][c.id] = (c, p_destino)

        # ------------------------------------------------------------------------------------------

        # c = Cliente_info()
        aresta_idxs = get_aresta_ids(mapa)

        # Obtendo as arestas de ida/chegada
        p_localizacao = marcar_ponto_cliente(c, mapa, qual = 'loc')
        # p_destino = marcar_ponto_cliente(c, mapa, qual = 'dest')
        
        c.p_local = p_localizacao[1]
        # c.p_destino = p_destino[1]

        # Marca o no do cliente no mapa
        node_cliente = get_novo_node_num(mapa)
        node_cliente_att = {'x': c.loc_x, 'y': c.loc_y, 'type': 'cliente', 'type_id': c.id}
        c.p1 = node_cliente

        mapa.add_node(node_cliente)
        mapa.nodes[node_cliente].update(node_cliente_att)

        # Marca o no de partida no mapa
        aresta = aresta_idxs[p_localizacao[0]]
        n1_att, n2_att = split_attributes(mapa, aresta=aresta, 
        x=c.p_local[0], y=c.p_local[1])

        node_att = {'x': c.p_local[0], 'y': c.p_local[1], 'type': 'partida', 'type_id': c.id}
        
        c.node_loc = get_novo_node_num(mapa)
        mapa = add_novo_node(mapa, aresta, novo_node_num=c.node_loc, 
        node_att=node_att, a1_att=n1_att, a2_att=n2_att)

        # Marca o no de destino no mapa
        aresta_idxs = get_aresta_ids(mapa) # Atualizando denovo

        p_destino = marcar_ponto_cliente(c, mapa, qual = 'dest')
        c.p_destino = p_destino[1]

        aresta = aresta_idxs[p_destino[0]]
        n1_att, n2_att = split_attributes(mapa, aresta=aresta, 
        x=c.p_destino[0], y=c.p_destino[1])

        node_att = {'x': c.p_destino[0], 'y': c.p_destino[1], 'type': 'destino', 'type_id': c.id}

        c.node_dest = get_novo_node_num(mapa)        
        mapa = add_novo_node(mapa, aresta, novo_node_num=c.node_dest, 
        node_att=node_att, a1_att=n1_att, a2_att=n2_att)

        lista_clientes.append(c)


    return mapa, lista_clientes


class caminho_info:

    def __init__(self) -> None:
        self.caminho = []
        self.tempo = 0
        
    def calcular_distancia_caminho(self, mapa: nx.DiGraph):
        dist = 0

        for node, idx in enumerate(self.caminho):
            if idx < len(self.caminho) - 1:
                dist += mapa[node][ self.caminho[idx + 1] ]['distancia']

            else:
                pass

        return dist

def obter_dist(p1: tuple, p2: tuple):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def listar_carros(mapa: nx.DiGraph, lista_carros: list, lista_clientes: list):
    """ Lista os carros e suas distancias de todos os clientes. """

    carros_info = dict() # Cada posicao, um carro, e pra cada carro, pega a distancia do cliente 

    for carro in lista_carros:
        # carro = Carro_info()

        # my_loc = (carro.loc_x, carro.loc_y)

        # Tempo, nao distancia
        # my_distance = obter_dist(my_loc, (carro.loc_x, carro.loc_y)) / mapa[carro.aresta_local[0]][carro.aresta_local[1]]['veloc'] * 60

        distance, shortest_distance, parent = dijkstra(mapa, carro.my_node)

        carros_info[carro.id] = dict()
        for cliente in lista_clientes:
            # cliente = Cliente_info()

            # cliente_loc = (cliente.p_local[1][0], cliente.p_local[1][1])

            # Tempo, nao distancia
            # client_dist = obter_dist((mapa.nodes[cliente.aresta_local[0]]['x'], mapa.nodes[cliente.aresta_local[0]]['y']), cliente_loc) / mapa[cliente.aresta_local[0]][cliente.aresta_local[1]]['veloc'] * 60

            cam_info = caminho_info()
            cam_info.caminho = backtrace(parent, carro.my_node, cliente.node_loc)
            cam_info.tempo = shortest_distance[cliente.node_loc]

            carros_info[carro.id][cliente.id] = cam_info

    return (lista_carros, carros_info)


def calcular_rota_cliente(mapa: nx.DiGraph, cl : Cliente_info):

    distance, shortest_distance, caminho = dijkstra(mapa, cl.aresta_local[1], cl.aresta_destino[0])
    cliente_loc = (cl.p_local[1][0], cl.p_local[1][1])
    cliente_dest = (cl.p_destino[1][0], cl.p_destino[1][1])

    # Tempo, nao distancia
    dist1 = obter_dist(cliente_loc, (mapa.nodes[cl.aresta_local[1]]['x'], mapa.nodes[cl.aresta_local[1]]['y'])) / mapa[cl.aresta_local[0]][cl.aresta_local[1]]['veloc'] * 60
    dist2 = obter_dist((mapa.nodes[cl.aresta_destino[0]]['x'], mapa.nodes[cl.aresta_destino[0]]['y']), cliente_dest) / mapa[cl.aresta_destino[0]][ cl.aresta_destino[1]]['veloc'] * 60

    # print(cl.aresta_local, mapa[cl.aresta_local[0]][cl.aresta_local[1]]['veloc'])
    # print(cl.aresta_destino, mapa[cl.aresta_destino[0]][ cl.aresta_destino[1]]['veloc'])
    # print("a ",cl.id, dist1, dist2) # a  543 2.7744870135828243 2.6879645495417797
    # a  443 2.7744870135828243 4.704899322409682
    # dist1 = dist2 = 0

    distancia_real = shortest_distance[cl.aresta_destino[0]] + dist1 + dist2

    return (caminho, distancia_real)


def calcular_rotas(mapa: nx.DiGraph, lista_clientes: list):
    
    for cliente in lista_clientes:
        cam, tempo = calcular_rota_cliente(mapa, cliente)

        print(cliente)
        print(cam, tempo)
