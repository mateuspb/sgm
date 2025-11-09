from django.db import models


class Tipocarga(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(null=True, blank=True)
    cor = models.CharField(max_length=7, default='#FFFFFF')
    data_criacao = models.DateTimeField(auto_now_add=True)
    ult_atualizacao = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
