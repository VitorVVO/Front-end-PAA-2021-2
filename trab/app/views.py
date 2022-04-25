from email.policy import default
from multiprocessing import context
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from .forms import *
from .models import *
from .grafo import *
from .algoritmo import *
from .p import *

# Create your views here.

def home(request):
    if request.method == 'POST':
        arq1, arq2, arq3 = 0, 0, 0
        if 'carros' in request.FILES.keys():
            uploaded_file = request.FILES['carros']
            fs = FileSystemStorage()
            name1 = fs.save(uploaded_file.name, uploaded_file)
            arq1 = name1
        if 'clientes' in request.FILES.keys():
            uploaded_file = request.FILES['clientes']
            fs = FileSystemStorage()
            name2 = fs.save(uploaded_file.name, uploaded_file)
            arq2 = name2
        if 'grafos' in request.FILES.keys():
            uploaded_file = request.FILES['grafos']
            fs = FileSystemStorage()
            name3 = fs.save(uploaded_file.name, uploaded_file)
            arq3 = name3

        if(arq1 == 0 or arq2 == 0 or arq3 == 0):
            messages.warning(request, 'Foram encontrados inconsistências no grafo, por favor corrigir.')
        else:
            if(insere_dado(arq1, arq2, arq3) == True):
                return tabelas(request)
            else:
                messages.warning(request, 'Foram encontrados inconsistências no grafo, por favor corrigir.')

    return render(request, 'app/upload.html')
    

def tabelas(request):
    carros = Carro.objects.all()
    clientes = Cliente.objects.all()
    grafos = Grafo.objects.all()

    return render(request, 'app/tabelas.html', {'carros':carros, 'clientes':clientes, 'grafos': grafos})

def simulacao(request, cliente, caminho):
    clientes = Cliente.objects.all().order_by('cliente_id')
    grafo = make_graph()

    grafo, lista_carros = marcar_carros(grafo)
    grafo, lista_clientes = marcar_clientes(grafo)

    id = cliente

    try:
        tempo_caminho = c_grafo(caminho, cliente, grafo, lista_carros, lista_clientes)
    except:
        messages.warning(request, 'Caminho inexistente')
        tempos_i, soma, count, tempos_carro_i, soma2, count2 = [], 0, 0, [], 0, 0
        for i in lista_clientes:
            carro_cliente = get_node_carro2(grafo, i.id, lista_carros, lista_clientes)
            caminhos, tempos = caminhos_mais_curtos(grafo, i.node_loc, i.node_dest, k=5, weight='weight')
            caminhos2, tempos_carro = caminhos_mais_curtos(grafo, carro_cliente, i.node_loc, k=5, weight='weight')
            tempos_i.append(tempos[0])
            tempos_carro_i.append(tempos_carro[0])

        for i in tempos_i:
            if i != 0:
                soma += i
                count += 1
        
        for i in tempos_carro_i:
            if i != 0:
                soma2 += i
                count2 += 1
        
        return render(request, 'app/simulacao.html', {'cliente':cliente,'caminho': 0, 'clientes':clientes, 'id':0, 'tempo_caminho':0,
                                                      'media_p':round(soma/count), 'q_clientes': count, 'media_c':round(soma2/count2)})

    tempos_i, soma, count, tempos_carro_i, soma2, count2 = [], 0, 0, [], 0, 0
    for i in lista_clientes:
        carro_cliente = get_node_carro2(grafo, i.id, lista_carros, lista_clientes)
        caminhos, tempos = caminhos_mais_curtos(grafo, i.node_loc, i.node_dest, k=5, weight='weight')
        caminhos2, tempos_carro = caminhos_mais_curtos(grafo, carro_cliente, i.node_loc, k=5, weight='weight')
        tempos_i.append(tempos[0])
        tempos_carro_i.append(tempos_carro[0])

    for i in tempos_i:
        if i != 0:
            soma += i
            count += 1
    
    for i in tempos_carro_i:
        if i != 0:
            soma2 += i
            count2 += 1
    

    return render(request, 'app/simulacao.html', {'cliente':cliente,'caminho': caminho, 'clientes':clientes, 'id':id, 
                                                    'media_p':round(soma/count), 'q_clientes': count, 'tempo_caminho': round(tempo_caminho),
                                                    'media_c':round(soma2/count2)})


def edit(request, tabela, id):
    if(tabela == 'carro'):
        carro = get_object_or_404(Carro, carro_id=id)
        form = CarroForm(instance=carro)
        title = 'Carro'

    elif(tabela == 'cliente'):
        cliente = get_object_or_404(Cliente, cliente_id=id)
        form = ClienteForm(instance=cliente)
        title = 'Cliente'

    elif(tabela == 'grafo'):
        grafo = get_object_or_404(Grafo, aresta_n=id)
        form = GrafoForm(instance=grafo)
        title = 'Grafo'

    if(request.method == 'POST'):
        if(title == 'Carro'):
            form = CarroForm(request.POST, instance=carro)
            form.save()
            return redirect('/tabelas')
        elif(title == 'Cliente'):
            form = ClienteForm(request.POST, instance=cliente)
            form.save()
            return redirect('/tabelas')
        elif(title == 'Grafo'):
            form = GrafoForm(request.POST, instance=grafo)
            form.save()
            return redirect('/tabelas')

    else:
        return render(request, 'app/edit.html', {'form': form, 'title': title})

def delete(request,tabela, id):
    if(tabela == 'carro'):
        carro = get_object_or_404(Carro, carro_id=id)
        carro.delete()

    elif(tabela == 'cliente'):
        cliente = get_object_or_404(Cliente, cliente_id=id)
        cliente.delete()

    elif(tabela == 'grafo'):
        grafo = get_object_or_404(Grafo, aresta_n=id)
        grafo.delete()

    return redirect('/tabelas')

def adicionar(request, tabela):
    if(request.method == "POST"):
        if(tabela == 'carro'):
            form = C_CarroForm(request.POST)
            form.save()

        elif(tabela == 'cliente'):
            form = C_ClienteForm(request.POST)
            form.save()

        elif(tabela == 'grafo'):
            form = C_GrafoForm(request.POST)
            form.save()

        return redirect('/tabelas')
    else:

        if(tabela == 'carro'):
            form = C_CarroForm()
    
        elif(tabela == 'cliente'):
            form = C_ClienteForm()

        elif(tabela == 'grafo'):
            form = C_GrafoForm()

        return render(request, 'app/adicionar.html', {'form': form, 'title':tabela})