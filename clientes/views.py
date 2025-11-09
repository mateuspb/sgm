from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from . import models, forms


class ClientesListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Cliente
    template_name = 'cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10
    permission_required = 'clientes.view_cliente'

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)

        return queryset


class ClientesCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Cliente
    template_name = 'cliente_create.html'
    form_class = forms.ClienteForm
    success_url = reverse_lazy('cliente_list')
    permission_required = 'clientes.add_cliente'


class ClientesDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Cliente
    template_name = 'cliente_detail.html'
    form_class = forms.ClienteForm
    success_url = reverse_lazy('cliente_list')
    permission_required = 'clientes.view_cliente'


class ClientesUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Cliente
    template_name = 'cliente_update.html'
    form_class = forms.ClienteForm
    success_url = reverse_lazy('cliente_list')
    permission_required = 'clientes.change_cliente'


class ClientesDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Cliente
    template_name = 'cliente_delete.html'
    success_url = reverse_lazy('cliente_list')
    permission_required = 'clientes.delete_cliente'
