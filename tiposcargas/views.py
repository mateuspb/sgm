from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from . import models, forms


class TiposcargasListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Tipocarga
    template_name = 'tipocarga_list.html'
    context_object_name = 'tiposcargas'
    paginate_by = 10
    permission_required = 'tiposcargas.view_tipocarga'

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)

        return queryset


class TiposcargasCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Tipocarga
    template_name = 'tipocarga_create.html'
    form_class = forms.TipocargaForm
    success_url = reverse_lazy('tipocarga_list')
    permission_required = 'tiposcargas.add_tipocarga'


class TiposcargasDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Tipocarga
    template_name = 'tipocarga_detail.html'
    form_class = forms.TipocargaForm
    success_url = reverse_lazy('tipocarga_list')
    permission_required = 'tiposcargas.view_tipocarga'


class TiposcargasUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Tipocarga
    template_name = 'tipocarga_update.html'
    form_class = forms.TipocargaForm
    success_url = reverse_lazy('tipocarga_list')
    permission_required = 'tiposcargas.change_tipocarga'


class TiposcargasDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Tipocarga
    template_name = 'tipocarga_delete.html'
    success_url = reverse_lazy('tipocarga_list')
    permission_required = 'tiposcargas.delete_tipocarga'
