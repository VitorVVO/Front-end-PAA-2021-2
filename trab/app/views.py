from multiprocessing import context
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

from app.forms import insere_dado
from .models import Carro
from .models import Cliente
from .models import Grafo

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

def simulacao(request):
    return render(request, 'app/simulacao.html')
