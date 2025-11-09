from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    cep = models.PositiveIntegerField(null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True, default='', db_index=True)
    cidade = models.CharField(max_length=100, null=True, blank=True, default='', db_index=True)
    bairro = models.CharField(max_length=100, null=True, blank=True, default='')
    endereco = models.CharField(max_length=100, null=True, blank=True, default='')
    numero = models.PositiveIntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True, default='')
    data_criacao = models.DateTimeField(auto_now_add=True)
    ult_atualizacao = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
