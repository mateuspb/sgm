from django.contrib import admin

from . import models


class MotoristaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnh')
    search_fields = ('nome',)


admin.site.register(models.Motorista, MotoristaAdmin)
