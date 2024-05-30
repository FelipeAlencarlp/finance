from django.shortcuts import render, redirect
from django.contrib import messages
from perfil.models import Categoria
from .models import ContaPagar, ContaPaga
from datetime import datetime


def definir_contas(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_contas.html', {'categorias': categorias})


def validar_dados(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        try:
            conta = ContaPagar(
                titulo = titulo,
                categoria_id=categoria,
                descricao=descricao,
                valor=valor,
                dia_pagamento=dia_pagamento
            )
            conta.save()

            messages.add_message(request, messages.SUCCESS, 'Conta cadastrada com sucesso')
            return redirect('/contas/definir_contas/')

        except:
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema! Contate um administrador.')
            return redirect('/contas/definir_contas/')


def ver_contas(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day
    contas = ContaPagar.objects.all()

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta') # traz os id's das contas pagas
    
    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas) # exclui as contas pagas da lista
    
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte=DIA_ATUAL + 5)\
        .filter(dia_pagamento__gt=DIA_ATUAL).exclude(id__in=contas_pagas) # traz conta com 5 dias para vencimento e exclui as vencidas ou pagas
    
    restantes = contas.exclude(id__in=contas_proximas_vencimento).exclude(id__in=contas_vencidas).exclude(id__in=contas_pagas)

    return render(request, 'ver_contas.html', {'contas_vencidas': contas_vencidas,
                                               'contas_proximas_vencimento': contas_proximas_vencimento,
                                               'restantes': restantes})