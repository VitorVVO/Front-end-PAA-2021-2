from email.policy import default
from multiprocessing import context
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from .forms import *
from .models import *
from .grafo import *

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

        insere_dado(arq1, arq2, arq3)
        return tabelas(request)

    return render(request, 'app/upload.html')
    

def tabelas(request):
    carros = Carro.objects.all()
    clientes = Cliente.objects.all()
    grafos = Grafo.objects.all()

    return render(request, 'app/tabelas.html', {'carros':carros, 'clientes':clientes, 'grafos': grafos})

def simulacao(request, caminho, cliente):
    clientes = Cliente.objects.all().order_by('cliente_id')
    c_grafo(cliente, caminho)
    return render(request, 'app/simulacao.html', {'cliente':cliente,'caminho': caminho, 'clientes':clientes})


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

    messages.info(request, 'Tarefa deletada com sucesso.')

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