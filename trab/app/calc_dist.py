import math

def calcula_km_nos (km_aresta, x_aresta1, y_aresta1, x_aresta2, y_aresta2, x_embarque1, y_embarque1):

    def distancia_entre_2_pontos(x_a, y_a, x_b, y_b):
        distancia = ((y_b - y_a) ** 2) + ((x_b - x_a) ** 2)
        distancia = math.sqrt(distancia)
        return (distancia)

    #calcula a distancia total da aresta e a distancia do ponto de embarque para os dois pontos da aresta
    Distancia_total_aresta = distancia_entre_2_pontos(x_aresta1, y_aresta1, x_aresta2, y_aresta2)
    Distancia_embarque_no1 = distancia_entre_2_pontos(x_embarque1, y_embarque1, x_aresta1, y_aresta1)
    Distancia_embarque_no2 = distancia_entre_2_pontos(x_embarque1, y_embarque1, x_aresta2, y_aresta2)

    # calcula os percentuais de destancia.
    percent_embarque_no1 = (Distancia_embarque_no1 / Distancia_total_aresta)
    percent_embarque_no2 = (Distancia_embarque_no2 / Distancia_total_aresta)

    # aplica os percentuais em ciam da kilometragem dada
    distancia_km1 = km_aresta * percent_embarque_no1
    distancia_km2 = km_aresta * percent_embarque_no2

    #retorna as duas distancias
    return(distancia_km1, distancia_km2)

# dist1, dist2 = calcula_km_nos (35, 3, 2, 9, 8, 5, 4)
# print(dist1, dist2, dist1+dist2)