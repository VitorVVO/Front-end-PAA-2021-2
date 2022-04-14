from django.db import models

# Create your models here.

class Carro(models.Model):
    carro_id = models.IntegerField(blank=False, null=False)
    loc_carro_x = models.FloatField(blank=False, null=False) 
    loc_carro_y = models.FloatField(blank=False, null=False)
    aresta_id = models.IntegerField(blank=False, null=False)

class Cliente(models.Model):

    cliente_id = models.IntegerField(blank=False, null=False)
    loc_cliente_x = models.FloatField(blank=False, null=False)
    loc_cliente_y = models.FloatField(blank=False, null=False)
    dest_cliente_x = models.FloatField(blank=False, null=False)
    dest_cliente_y = models.FloatField(blank=False, null=False)

class Grafo(models.Model):
    aresta_n = models.IntegerField(blank=False, null=False, default=0)
    v_origem = models.IntegerField(blank=False, null=False, default=0)
    loc_v_origem_x = models.FloatField(blank=False, null=False, default=0)
    loc_v_origem_y = models.FloatField(blank=False, null=False, default=0)
    v_destino = models.IntegerField(blank=False, null=False, default=0)
    loc_v_destino_x = models.FloatField(blank=False, null=False, default=0)
    loc_v_destino_y = models.FloatField(blank=False, null=False, default=0)
    distancia_km = models.FloatField(blank=False, null=False, default=0)
    velocidade_km_h = models.IntegerField(blank=False, null=False, default=0)
