from django.urls import path
from . import views

urlpatterns = [
    path('novo_valor/', views.novo_valor, name='novo_valor'),
    path('verifica_dados/', views.verifica_dados, name='verifica_dados'),
    path('view_extrato/', views.view_extrato, name='view_extrato'),
    path('exportar_pdf/', views.exportar_pdf, name='exportar_pdf'),
]