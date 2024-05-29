from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from perfil.models import Categoria
from extrato.models import Valores
from perfil.utils import calcula_total
import json


def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})


def ver_planejamento(request):
    categorias = Categoria.objects.all()
    valores = Valores.objects.all()

    total_categorias = calcula_total(categorias, 'valor_planejamento')
    total_valores = calcula_total(valores, 'valor')

    percentual_permitido = int((total_valores * 100) / total_categorias)

    return render(request, 'ver_planejamento.html', {'categorias': categorias,
                                                     'total_categorias': total_categorias,
                                                     'percentual_permitido': percentual_permitido})


@csrf_exempt
def update_valor_categoria(request, categoria_id):
    novo_valor = json.load(request)['novo_valor'] # converte toda a requisição em json e acessa o que veio do front
    categoria = Categoria.objects.get(id=categoria_id)

    categoria.valor_planejamento = novo_valor
    categoria.save()
   
    return JsonResponse({'status': 'Sucesso'})