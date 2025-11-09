from django.contrib import admin

from . import models


class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'cliente', 'peso_carregado', 'motorista', 'produto', 'observacoes', 'tipo_carga', 'situacao')
    search_fields = ('cliente__nome',)


admin.site.register(models.Movimentacao, MovimentacaoAdmin)
