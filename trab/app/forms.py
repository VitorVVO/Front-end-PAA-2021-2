from django import forms
from .models import Carro, Cliente, Grafo

def validacao(arq, n):
    return True
    lines = arq.readlines()
    vals_id = []
    if n == 1:
        cabecalho = lines[0].split()
        if(cabecalho != ['Carro_id','loc_carro_x','loc_carro_y','aresta_id']):
            return False
        for i in range(1,len(lines)):
            vals = lines[i].split()
            if len(vals) != 4:
                return False
            if (vals_id.count(vals[0]) == 0):
                vals_id.append(vals[0]) 
            else: 
               return False  
        return True 

    elif n == 2:
        cabecalho = lines[0].split()
        if(cabecalho != ['Cliente_id', 'loc_cliente_x', 'loc_cliente_y', 'dest_cliente_x', 'dest_cliente_y']):
            return False
        for i in range(1,len(lines)):
            vals = lines[i].split()
            if len(vals) != 5:
                return False
            if (vals_id.count(vals[0]) == 0):
               vals_id.append(vals[0]) 
            else: 
               return False  

        return True
    
    
    elif n == 3:
        cabecalho = lines[0].split()
        if(cabecalho != ['Aresta_n', 'v_origem', 'Loc_v_origem_x', 'Loc_v_origem_y', 'v_destino', 'Loc_v_destino_x', 'Loc_v_destino_y', 'Distância_km', 'Velocidade_km_h']):
            return False
        for i in range(1,len(lines)):
            vals = lines[i].split()
            if len(vals) != 9:
                return False
            if (vals_id.count(vals[0]) == 0):
               vals_id.append(vals[0]) 
            else: 
               return False 

        return True
    
def insere_dado(arq1, arq2, arq3):
    file_path = 'media'
    arquivo1 = open(file_path + '/' + arq1)
    arquivo2 = open(file_path + '/' + arq2)
    arquivo3 = open(file_path + '/' + arq3)

    if(validacao(arquivo1, 1)):
        count = 0
        for i in arquivo1:
            if(count != 0):
                val = i.split()
                Carro.objects.create(carro_id = int(val[0]), loc_carro_x = float(val[1]), loc_carro_y = float(val[2]) , aresta_id = int(val[3]))
            count +=1
    if(validacao(arquivo2, 2)):
        count = 0
        for i in arquivo2:
            if(count != 0):
                val = i.split()
                Cliente.objects.create(cliente_id = int(val[0]), loc_cliente_x = float(val[1]), loc_cliente_y = float(val[2]),
                                        dest_cliente_x = float(val[3]), dest_cliente_y = float(val[4]))
            count +=1
    if(validacao(arquivo3, 3)):
        count = 0
        for i in arquivo3:
            if(count != 0):
                val = i.split()
                Grafo.objects.create(aresta_n = int(val[0]), v_origem = int(val[1]), loc_v_origem_x = float(val[2]),
                                    loc_v_origem_y = float(val[3]), v_destino = int(val[4]), loc_v_destino_x = float(val[5]), loc_v_destino_y = float(val[6]), 
                                    distancia_km = float(val[7]), velocidade_km_h = int(val[8]))
            count +=1
    

class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = ('loc_carro_x', 'loc_carro_y', 'aresta_id')

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('loc_cliente_x', 'loc_cliente_y', 'dest_cliente_x', 'dest_cliente_y')

class GrafoForm(forms.ModelForm):
    class Meta:
        model = Grafo
        fields = ('v_origem', 'loc_v_origem_x', 'loc_v_origem_y', 'v_destino', 'loc_v_destino_x', 'loc_v_destino_y', 'distancia_km', 'velocidade_km_h')

class C_CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = ('carro_id','loc_carro_x', 'loc_carro_y', 'aresta_id')

class C_ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('cliente_id', 'loc_cliente_x', 'loc_cliente_y', 'dest_cliente_x', 'dest_cliente_y')

class C_GrafoForm(forms.ModelForm):
    class Meta:
        model = Grafo
        fields = ('aresta_n','v_origem', 'loc_v_origem_x', 'loc_v_origem_y', 'v_destino', 'loc_v_destino_x', 'loc_v_destino_y', 'distancia_km', 'velocidade_km_h')