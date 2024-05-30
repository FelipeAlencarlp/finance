from django.db.models import Sum
from datetime import datetime

def calcula_total(objeto, campo):
    # total = 0
    # for i in objeto:
    #     total += getattr(i, campo)

    # mesma forma que de cima, só que mais enxuta
    total = objeto.aggregate(Sum(campo))[campo + '__sum']

    if total == None: total = 0

    return total


def calcula_equilibrio_financeiro():
    from extrato.models import Valores
    
    gastos_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=False)

    total_gastos_essenciais = calcula_total(gastos_essenciais, 'valor')
    total_gastos_nao_essenciais = calcula_total(gastos_nao_essenciais, 'valor')

    total = total_gastos_essenciais + total_gastos_nao_essenciais
    try:
        percentual_gastos_essenciais = (total_gastos_essenciais * 100) / total
        percentual_gastos_nao_essenciais = (total_gastos_nao_essenciais * 100) / total

        return percentual_gastos_essenciais, percentual_gastos_nao_essenciais
    except:
        return 0, 0
    
