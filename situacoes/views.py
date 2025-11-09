from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from . import models, forms


class SituacoesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Situacao
    template_name = 'situacao_list.html'
    context_object_name = 'situacoes'
    paginate_by = 10
    permission_required = 'situacoes.view_situacao'

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)

        return queryset


class SituacoesCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Situacao
    template_name = 'situacao_create.html'
    form_class = forms.SituacaoForm
    success_url = reverse_lazy('situacao_list')
    permission_required = 'situacoes.add_situacao'


class SituacoesDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Situacao
    template_name = 'situacao_detail.html'
    form_class = forms.SituacaoForm
    success_url = reverse_lazy('situacao_list')
    permission_required = 'situacoes.view_situacao'


class SituacoesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Situacao
    template_name = 'situacao_update.html'
    form_class = forms.SituacaoForm
    success_url = reverse_lazy('situacao_list')
    permission_required = 'situacoes.change_situacao'


class SituacoesDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Situacao
    template_name = 'situacao_delete.html'
    success_url = reverse_lazy('situacao_list')
    permission_required = 'situacoes.delete_situacao'
