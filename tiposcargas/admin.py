from django.contrib import admin

from . import models


class TipocargaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)


admin.site.register(models.Tipocarga, TipocargaAdmin)
