from rest_framework import serializers

from movimentacoes.models import Movimentacao


class MovimentacaoSerializer(serializers.ModelSerializer):
    motorista_nome = serializers.CharField(source='motorista.nome', read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    veiculo_placa = serializers.CharField(source='veiculo.placa', read_only=True)
    tipo_carga_nome = serializers.CharField(source='tipo_carga.nome', read_only=True)
    situacao_nome = serializers.CharField(source='situacao.nome', read_only=True)

    class Meta:
        model = Movimentacao
        fields = [
            'id', 'veiculo', 'cliente', 'peso_carregado', 'motorista',
            'produto', 'observacoes', 'tipo_carga', 'situacao',
            'assinatura_base64', 'data_assinatura', 'data_criacao',
            'cliente_nome', 'produto_nome', 'motorista_nome',
            'veiculo_placa', 'tipo_carga_nome', 'situacao_nome'
        ]
