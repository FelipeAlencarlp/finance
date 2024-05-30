from django.urls import path
from . import views

urlpatterns = [
    path('definir_contas/', views.definir_contas, name='definir_contas'),
    path('validar_dados/', views.validar_dados, name='validar_dados'),
    path('ver_contas/', views.ver_contas, name='ver_contas'),
]