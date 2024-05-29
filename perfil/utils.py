from django.db.models import Sum

def calcula_total(objeto, campo):
    # total = 0
    # for i in objeto:
    #     total += getattr(i, campo)

    # mesma forma que de cima, só que mais enxuta
    total = objeto.aggregate(Sum(campo))[campo + '__sum']

    if total == None: total = 0

    return total

