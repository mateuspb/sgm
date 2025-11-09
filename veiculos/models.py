from django.db import models


class Veiculo(models.Model):
    placa = models.CharField(max_length=7)
    modelo = models.CharField(max_length=100)
    ano = models.PositiveIntegerField()
    carga_total = models.DecimalField(max_digits=14, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ult_atualizacao = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.placa

    class Meta:
        ordering = ['placa']
