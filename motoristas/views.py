from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from . import models, forms


class MotoristasListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Motorista
    template_name = 'motorista_list.html'
    context_object_name = 'motoristas'
    paginate_by = 10
    permission_required = 'motoristas.view_motorista'

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)

        return queryset


class MotoristasCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Motorista
    template_name = 'motorista_create.html'
    form_class = forms.MotoristaForm
    success_url = reverse_lazy('motorista_list')
    permission_required = 'motoristas.add_motorista'


class MotoristasDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Motorista
    template_name = 'motorista_detail.html'
    form_class = forms.MotoristaForm
    success_url = reverse_lazy('motorista_list')
    permission_required = 'motoristas.view_motorista'


class MotoristasUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Motorista
    template_name = 'motorista_update.html'
    form_class = forms.MotoristaForm
    success_url = reverse_lazy('motorista_list')
    permission_required = 'motoristas.change_motorista'


class MotoristasDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Motorista
    template_name = 'motorista_delete.html'
    success_url = reverse_lazy('motorista_list')
    permission_required = 'motoristas.delete_motorista'
