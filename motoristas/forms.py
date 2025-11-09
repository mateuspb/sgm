from django import forms

from . import models


class MotoristaForm(forms.ModelForm):
    class Meta:
        model = models.Motorista
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnh': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome',
            'cnh': 'CNH',
        }
