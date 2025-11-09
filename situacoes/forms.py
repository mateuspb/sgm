from django import forms

from . import models


class SituacaoForm(forms.ModelForm):
    class Meta:
        model = models.Situacao
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cor': forms.TextInput(attrs={'class': 'form-control form-control-color', 'type': "color"}),
        }
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'cor': 'Cor',
        }
