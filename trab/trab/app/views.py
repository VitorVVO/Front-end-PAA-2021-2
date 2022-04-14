from multiprocessing import context
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage

# Create your views here.

def home(request):
    context = {}
    if request.method == 'POST':
        if 'carros' in request.FILES.keys():
            uploaded_file = request.FILES['carros']
            car_arq = uploaded_file.name
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            context['url'] = fs.url(name)
        if 'clientes' in request.FILES.keys():
            uploaded_file = request.FILES['clientes']
            cl_arq = uploaded_file.name
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            context['url2'] = fs.url(name)
        if 'grafos' in request.FILES.keys():
            uploaded_file = request.FILES['grafos']
            gr_arq = uploaded_file.name
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name, uploaded_file)
            context['url3'] = fs.url(name)

    return render(request, 'app/upload.html', context)
    

def simulacao(request):
    return render(request, 'app/simulacao.html')
