from django.db import models

from clientes.models import Cliente
from motoristas.models import Motorista
from produtos.models import Produto
from situacoes.models import Situacao
from tiposcargas.models import Tipocarga
from veiculos.models import Veiculo


class Movimentacao(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name='movimentacoes')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='movimentacoes')
    peso_carregado = models.DecimalField(max_digits=14, decimal_places=2)
    motorista = models.ForeignKey(Motorista, on_delete=models.PROTECT, related_name='movimentacoes')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='movimentacoes')
    observacoes = models.TextField(max_length=200, blank=True, null=True, default="")
    tipo_carga = models.ForeignKey(Tipocarga, on_delete=models.PROTECT, related_name='movimentacoes')
    situacao = models.ForeignKey(Situacao, on_delete=models.PROTECT, related_name='movimentacoes')
    assinatura_base64 = models.TextField(blank=True, null=True, default="")
    data_assinatura = models.DateTimeField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ult_atualizacao = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return f"Comprovante #{self.id}"

    class Meta:
        ordering = ['-id']
