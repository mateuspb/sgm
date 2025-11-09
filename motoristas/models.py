from django.db import models


class Motorista(models.Model):
    nome = models.CharField(max_length=100)
    cnh = models.CharField(max_length=20)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ult_atualizacao = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
