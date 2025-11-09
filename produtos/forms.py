from django import forms

from . import models


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = models.Produto
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
        }
