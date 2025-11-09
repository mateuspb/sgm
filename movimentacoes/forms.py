from django import forms

from . import models


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = models.Movimentacao
        fields = [
            "veiculo", "cliente", "peso_carregado", "motorista",
            "produto", "observacoes", "tipo_carga", "situacao",
        ]
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'peso_carregado': forms.NumberInput(attrs={'class': 'form-control'}),
            'motorista': forms.Select(attrs={'class': 'form-control'}),
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_carga': forms.Select(attrs={'class': 'form-control'}),
            'situacao': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'veiculo': 'Placa',
            'cliente': 'Cliente',
            'peso_carregado': 'Peso Carregado',
            'motorista': 'Motorista',
            'produto': 'Produto',
            'observacoes': 'Observações',
            'tipo_carga': 'Tipo de Carga',
            'situacao': 'Situação',
        }
