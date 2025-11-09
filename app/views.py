import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import painel


@login_required(login_url='login')
def home(request):
    movimentacoes_dados = painel.get_painel_movimentacao()
    grafico_valor_vendas_diarias = painel.get_dados_valor_vendas_diarias()
    grafico_quantidade_vendas_diarias = painel.get_dados_quantidade_vendas_diarias()

    context = {
        'movimentacoes_dados': movimentacoes_dados,
        'dados_valor_vendas_diarias': json.dumps(grafico_valor_vendas_diarias),
        'dados_quantidade_vendas_diarias': json.dumps(grafico_quantidade_vendas_diarias),
    }

    return render(request, 'home.html', context)
