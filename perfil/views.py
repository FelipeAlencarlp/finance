from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum

from .models import Conta, Categoria
from .utils import calcula_total


def home(request):
    contas = Conta.objects.all()
    saldo_total = calcula_total(contas, 'valor')
    return render(request, 'home.html', {'contas': contas,
                                         'saldo_total': saldo_total})


def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    total_contas = calcula_total(contas, 'valor')
    # total_contas = contas.aggregate(Sum('valor'))['valor__sum'] # soma a columa valor
    
    return render(request, 'gerenciar.html', {'contas': contas,
                                              'total_contas': total_contas,
                                              'categorias': categorias})


def cadastrar_banco(request):
    if request.method == 'POST':
        apelido = request.POST.get('apelido')
        banco = request.POST.get('banco')
        tipo = request.POST.get('tipo')
        valor = request.POST.get('valor')
        icone = request.FILES.get('icone')
        
        if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
            messages.add_message(request, messages.ERROR, 'Preencha todos os campos')
            return redirect('/perfil/gerenciar/')
        
        try:
            conta = Conta(
                apelido = apelido,
                banco=banco,
                tipo=tipo,
                valor=valor,
                icone=icone
            )

            conta.save()

            messages.add_message(request, messages.SUCCESS, 'Banco cadastrado com sucesso!')
            return redirect('/perfil/gerenciar/')
        
        except:
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema! Contate um administrador.')
            return redirect('/perfil/gerenciar/')


def deletar_banco(request, banco_id):
    try:
        conta = get_object_or_404(Conta, id=banco_id)
        conta.delete()
        
        messages.add_message(request, messages.SUCCESS, 'Conta removida com sucesso')
        return redirect('/perfil/gerenciar/')
    
    except:
        messages.add_message(request, messages.ERROR, 'Erro interno no sistema! Contate um administrador.')
        return redirect('/perfil/gerenciar/')


def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    if len(nome.strip()) == 0:
        messages.add_message(request, messages.ERROR, 'Preencha o campo Categoria')
        return redirect('/perfil/gerenciar/')

    try:
        categoria = Categoria(
            categoria=nome,
            essencial=essencial
        )

        categoria.save()

        messages.add_message(request, messages.SUCCESS, 'Categoria cadastrada com sucesso')
        return redirect('/perfil/gerenciar/')
    
    except:
        messages.add_message(request, messages.ERROR, 'Erro interno no sistema! Contate um administrador.')
        return redirect('/perfil/gerenciar/')


def update_categoria(request, categoria_id):
    try:
        categoria = get_object_or_404(Categoria, id=categoria_id)

        categoria.essencial = not categoria.essencial
        categoria.save()

        messages.add_message(request, messages.SUCCESS, 'Categoria alterada com sucesso')
        return redirect('/perfil/gerenciar/')

    except:
        messages.add_message(request, messages.ERROR, 'Erro interno no sistema! Contate um administrador.')
        return redirect('/perfil/gerenciar/')
