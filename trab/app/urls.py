from unicodedata import name
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('simulacao/<imagem>/', views.simulacao, name='simulacao'),
    path('tabelas', views.tabelas, name='tabelas'),
    path('edit/<str:tabela>/<int:id>', views.edit, name='edit'),
    path('delete/<str:tabela>/<int:id>', views.delete, name='delete'),
    path('adicionar/<str:tabela>', views.adicionar, name='adicionar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)