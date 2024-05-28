from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from perfil.models import Conta, Categoria
from .models import Valores


def novo_valor(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    return render(request, 'novo_valor.html', {'contas': contas, 'categorias': categorias})


def verifica_dados(request):
    if request.method == 'POST':
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')

        try:
            valores = Valores(
                valor=valor,
                categoria_id=categoria,
                descricao=descricao,
                data=data,
                conta_id=conta,
                tipo=tipo,
            )

            valores.save()

            conta = get_object_or_404(Conta, id=conta)

            if tipo == 'E':
                conta.valor += float(valor)
            else:
                conta.valor -= float(valor)

            conta.save()

            if tipo == 'E':
                messages.add_message(request, messages.SUCCESS, 'Entrada cadastrada com sucesso')
            else:
                messages.add_message(request, messages.SUCCESS, 'Saída cadastrada com sucesso')

            return redirect('/extrato/novo_valor/')

        except:
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema! Contate um administrador.')
            return redirect('/extrato/novo_valor/')


def view_extrato(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    valores = Valores.objects.filter(data__month=datetime.now().month) # tras somente de cada mês

    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')

    # filtros
    if conta_get:
        valores = valores.filter(conta__id=conta_get)

    if categoria_get:
        valores = valores.filter(categoria__id=categoria_get)

    

 
    return render(request, 'view_extrato.html', {'valores': valores,
                                                 'contas': contas,
                                                 'categorias': categorias})
