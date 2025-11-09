from django import forms

from . import models


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = models.Veiculo
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'carga_total': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome',
            'modelo': 'Modelo',
            'ano': 'Ano',
            'carga_total': 'Carga Total',
        }
