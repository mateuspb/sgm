import base64
import io
import os
import json

from django.http import FileResponse, Http404, JsonResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.staticfiles import finders
from django.db.models import Q

# API
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

# para gerar PDF e gráficos
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

from . import models, forms, serializers


class MovimentacoesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Movimentacao
    template_name = 'movimentacao_list.html'
    context_object_name = 'movimentacoes'
    paginate_by = 10
    permission_required = 'movimentacoes.view_movimentacao'

    def get_queryset(self):
        queryset = super().get_queryset()
        cliente = self.request.GET.get('cliente')

        if cliente:
            queryset = queryset.filter(cliente__nome__icontains=cliente)

        return queryset


class MovimentacoesCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Movimentacao
    template_name = 'movimentacao_create.html'
    form_class = forms.MovimentacaoForm
    success_url = reverse_lazy('movimentacao_list')
    permission_required = 'movimentacoes.add_movimentacao'


class MovimentacoesDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Movimentacao
    template_name = 'movimentacao_detail.html'
    form_class = forms.MovimentacaoForm
    success_url = reverse_lazy('movimentacao_list')
    permission_required = 'movimentacoes.view_movimentacao'


class MovimentacoesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Movimentacao
    template_name = 'movimentacao_update.html'
    form_class = forms.MovimentacaoForm
    success_url = reverse_lazy('movimentacao_list')
    permission_required = 'movimentacoes.change_movimentacao'


class MovimentacoesDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Movimentacao
    template_name = 'movimentacao_delete.html'
    success_url = reverse_lazy('movimentacao_list')
    permission_required = 'movimentacoes.delete_movimentacao'


class MovimentacoesAPIView(viewsets.ModelViewSet):
    queryset = models.Movimentacao.objects.all().order_by('-data_criacao')
    serializer_class = serializers.MovimentacaoSerializer

    # LIST action (sem pk) => /movimentacoes/assinaturas-pendentes/
    @action(detail=False, methods=['get'], url_path='assinaturas-pendentes')
    def assinaturas_pendentes(self, request):
        qs = models.Movimentacao.objects.filter(Q(assinatura_base64__isnull=True) | Q(assinatura_base64__exact="")).exclude(situacao=2).select_related('cliente', 'motorista', 'produto', 'veiculo', 'tipo_carga', 'situacao').order_by('-data_criacao')
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    # DETAIL action (com pk) => /movimentacoes/{id}/assinar/
    @action(detail=True, methods=['patch'], url_path='assinar')
    def assinar(self, request, pk=None):
        mov = self.get_object()

        assinatura = request.data.get("assinatura_base64")
        if not assinatura:
            return Response({"detail": "assinatura_base64 obrigatória"}, status=status.HTTP_400_BAD_REQUEST)

        data_ass = request.data.get("data_assinatura")
        if not data_ass:
            return Response({"detail": "data_assinatura obrigatória"}, status=status.HTTP_400_BAD_REQUEST)

        mov.assinatura_base64 = assinatura
        mov.data_assinatura = data_ass
        mov.save(update_fields=["assinatura_base64", "data_assinatura"])
        return Response(self.get_serializer(mov).data, status=status.HTTP_200_OK)


@csrf_exempt
@require_POST
def salvar_assinatura(request):
    data = json.loads(request.body)
    try:
        mov = models.Movimentacao.objects.get(pk=data['id'])
        mov.assinatura_base64 = data['assinatura']
        mov.data_assinatura = timezone.now()
        mov.save()
        return JsonResponse({'mensagem': 'Assinatura salva com sucesso!'})
    except models.Movimentacao.DoesNotExist:
        return JsonResponse({'erro': 'Movimentação não encontrada'}, status=404)


def gerar_pdf(request, id):
    try:
        mov = models.Movimentacao.objects.select_related('veiculo', 'cliente', 'motorista', 'produto').get(pk=id)
    except models.Movimentacao.DoesNotExist:
        raise Http404("Movimentação não encontrada")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    margem = 20 * mm
    coluna1_x = margem
    coluna2_x = largura / 2 + 10 * mm
    y = altura - margem

    # 1. Ponto mais alto (topo do conteúdo)
    margem_superior = altura - margem

    # Logo
    logo_candidates = ['image/logo.png', 'logo.png']
    logo_path = None

    for rel in logo_candidates:
        found = finders.find(rel)
        if found:
            logo_path = found
            break

    if not logo_path:
        for rel in logo_candidates:
            candidate = os.path.join(settings.BASE_DIR, 'static', rel)
            if os.path.exists(candidate):
                logo_path = candidate
                break

    # Desenha se encontrado
    if logo_path:
        p.drawImage(logo_path, coluna1_x, y - 50, width=50, preserveAspectRatio=True, mask='auto')
    else:
        # Opcional: log para facilitar debug
        print("Logo não encontrado em:", logo_candidates)

    # Coluna 1
    y -= 60
    p.setFont("Helvetica", 10)
    p.drawString(coluna1_x, y, "CLIENTE: ")

    p.setFont("Helvetica-Bold", 10)
    text_width = p.stringWidth("CLIENTE: ", "Helvetica", 10)
    p.drawString(coluna1_x + text_width, y, mov.cliente.nome)

    y -= 15
    p.setFont("Helvetica", 10)
    p.drawString(coluna1_x, y, "PRODUTO: ")

    p.setFont("Helvetica-Bold", 10)
    text_width = p.stringWidth("PRODUTO: ", "Helvetica", 10)
    p.drawString(coluna1_x + text_width, y, mov.produto.nome)

    y -= 30
    p.setFont("Helvetica", 10)
    p.drawString(coluna1_x, y, "MOTORISTA: ")

    p.setFont("Helvetica-Bold", 10)
    text_width = p.stringWidth("MOTORISTA: ", "Helvetica", 10)
    p.drawString(coluna1_x + text_width, y, mov.motorista.nome)

    y -= 15
    p.setFont("Helvetica", 10)
    p.drawString(coluna1_x, y, f"PLACA: {mov.veiculo.placa}")

    y -= 15
    p.setFont("Helvetica", 10)
    p.drawString(coluna1_x, y, f"OBS: {mov.observacoes or '-'}")

    y -= 60
    p.setFont("Helvetica-Bold", 12)
    p.drawString(coluna1_x, y, f"{mov.id:09d}")

    # Coluna 2
    y2 = altura - margem

    texto = "COMPROVANTE DE PESAGEM"
    fonte = "Helvetica-Bold"
    tamanho_fonte = 12

    p.setFont(fonte, tamanho_fonte)

    # centralizar
    largura_pagina, _ = A4
    largura_texto = p.stringWidth(texto, fonte, tamanho_fonte)
    x2_central = ((largura_pagina - largura_texto - margem) + coluna2_x) / 2

    p.setFont(fonte, tamanho_fonte)
    p.drawString(x2_central, y2 - 30, texto)

    # Calcular largura do texto
    largura_texto = p.stringWidth(texto, fonte, tamanho_fonte)

    # Desenhar sublinhado logo abaixo
    linha_y = y2 - 32  # Ajuste fino da altura da linha
    p.setLineWidth(1)
    p.line(x2_central, linha_y, x2_central + largura_texto, linha_y)

    y2 -= 30
    texto = f"Data/Hora: {mov.data_criacao.strftime('%d/%m/%Y %H:%M')}"
    fonte = "Helvetica-Bold"
    tamanho_fonte = 10

    p.setFont(fonte, tamanho_fonte)

    # centralizar
    largura_texto = p.stringWidth(texto, fonte, tamanho_fonte)

    x2_central = ((largura_pagina - largura_texto - margem) + coluna2_x) / 2
    y2 -= 15
    p.drawString(x2_central, y2, texto)

    y2 -= 30
    p.setFont("Helvetica", 10)
    p.drawString(coluna2_x, y2, "PRIMEIRA PESAGEM: ")

    p.setFont("Helvetica-Bold", 10)
    text_width = p.stringWidth("PRIMEIRA PESAGEM: ", "Helvetica", 10)
    p.drawString(coluna2_x + text_width, y2, f"{mov.veiculo.carga_total:.3f} KG")

    y2 -= 15
    p.setFont("Helvetica", 10)
    p.drawString(coluna2_x, y2, "SEGUNDA PESAGEM: ")

    p.setFont("Helvetica-Bold", 10)
    text_width = p.stringWidth("SEGUNDA PESAGEM: ", "Helvetica", 10)
    p.drawString(coluna2_x + text_width, y2, f"{mov.peso_carregado:.3f} KG")

    y2 -= 15
    p.setFont("Helvetica", 10)
    p.drawString(coluna2_x, y2, "LÍQUIDO: ")

    p.setFont("Helvetica-Bold", 10)
    text_width = p.stringWidth("LÍQUIDO: ", "Helvetica", 10)
    peso_liquido = mov.peso_carregado - mov.veiculo.carga_total
    p.drawString(coluna2_x + text_width, y2, f"{peso_liquido:.3f} KG")

    # Assinatura (base64)
    if mov.assinatura_base64:
        try:
            # Garante que a assinatura é tratada mesmo com ou sem prefixo
            assinatura_data = mov.assinatura_base64
            if "base64," in assinatura_data:
                assinatura_data = assinatura_data.split("base64,")[1]

            assinatura_bytes = base64.b64decode(assinatura_data)
            assinatura_image = ImageReader(io.BytesIO(assinatura_bytes))

            # centralizar assinatura
            largura_assinatura = 200
            x2_assinatura_central = ((largura_pagina - largura_assinatura - margem) + coluna2_x) / 2

            linha_y = y2 - 110  # Ajuste fino da altura da linha
            p.setLineWidth(1)
            p.line(x2_assinatura_central, linha_y, x2_assinatura_central + 200, linha_y)

            p.drawImage(assinatura_image, x2_assinatura_central + 25, y2 - 100, width=150, height=50, mask='auto')

        except Exception as e:
            print("Erro ao carregar assinatura:", e)

    y2 -= 120
    # Desenhar centralizado e sublinhado logo abaixo
    texto = "Assinatura"
    fonte = "Helvetica"
    tamanho_fonte = 10

    p.setFont(fonte, tamanho_fonte)

    # centralizar
    largura_texto = p.stringWidth(texto, fonte, tamanho_fonte)

    x2_central = ((largura_pagina - largura_texto - margem) + coluna2_x) / 2
    p.drawString(x2_central, y2, texto)

    # tamanho da margem inferior utilizada
    margem_inferior_conteudo = min(y, y2)

    # Adicione um pequeno padding (5 mm)
    padding = 5 * mm
    x_inicial = coluna1_x - padding
    y_inicial = margem_inferior_conteudo - padding
    largura_moldura = (largura - 2 * margem) + 2 * padding
    altura_moldura = (margem_superior - margem_inferior_conteudo) + 2 * padding

    # 4. Desenha moldura apenas ao redor do conteúdo usado
    p.setStrokeColorRGB(0.2, 0.2, 0.2)
    p.setLineWidth(1)
    p.rect(x_inicial, y_inicial, largura_moldura, altura_moldura)

    p.showPage()
    p.save()
    buffer.seek(0)

    nome_pdf = "comprovante_de_pesagem_" + f"{mov.id:09d}" + "_" + mov.data_criacao.strftime('%d-%m-%Y_%H-%M') + ".pdf"

    return FileResponse(buffer, as_attachment=False, filename=nome_pdf)
