from unicodedata import name
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('simulacao/<imagem>/', views.simulacao, name='simulacao'),
    path('tabelas', views.tabelas, name='tabelas')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)