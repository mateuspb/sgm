from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ult_atualizacao = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
