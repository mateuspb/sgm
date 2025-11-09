from django.contrib import admin

from . import models


class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modelo', 'ano', 'carga_total')
    search_fields = ('placa',)


admin.site.register(models.Veiculo, VeiculoAdmin)
