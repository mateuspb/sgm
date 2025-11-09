from django.db.models import Sum, F
from django.utils.formats import number_format
from django.utils import timezone
from movimentacoes.models import Movimentacao


def get_painel_movimentacao():
    quantidade_total = Movimentacao.objects.filter(situacao=3).count()
    movimentacoes = Movimentacao.objects.filter(situacao=3)
    peso_total = sum(movimentacao.peso_carregado - movimentacao.veiculo.carga_total for movimentacao in movimentacoes)

    return dict(
        quantidade_total=quantidade_total,
        peso_total=number_format(peso_total, decimal_pos=3, force_grouping=True),
    )


def get_dados_valor_vendas_diarias():
    today = timezone.now().date()
    datas = [str(today - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    valores = list()

    for data in datas:
        vendas_total = Movimentacao.objects.filter(
            situacao=3, data_criacao__date=data
        ).aggregate(
            total_vendas=Sum(F('produto__preco') * (F('peso_carregado') - F('veiculo__carga_total')))
        )['total_vendas'] or 0
        valores.append(float(vendas_total))

    return dict(
        datas=datas,
        valores=valores,
    )


def get_dados_quantidade_vendas_diarias():
    today = timezone.now().date()
    datas = [str(today - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    quantidades = list()

    for data in datas:
        quantidades_vendas = Movimentacao.objects.filter(situacao=3, data_criacao__date=data).count()
        quantidades.append(quantidades_vendas)
    print(quantidades)
    return dict(
        datas=datas,
        quantidades=quantidades,
    )
