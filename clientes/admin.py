from django.contrib import admin
from . import models


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'cep', 'cidade', 'bairro', 'endereco', 'numero', 'complemento')
    search_fields = ('nome',)


admin.site.register(models.Cliente, ClienteAdmin)
