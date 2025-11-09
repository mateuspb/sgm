from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from . import models, forms


class VeiculosListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Veiculo
    template_name = 'veiculo_list.html'
    context_object_name = 'veiculos'
    paginate_by = 10
    permission_required = 'veiculos.view_veiculo'

    def get_queryset(self):
        queryset = super().get_queryset()
        placa = self.request.GET.get('placa')

        if placa:
            queryset = queryset.filter(placa__icontains=placa)

        return queryset


class VeiculosCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Veiculo
    template_name = 'veiculo_create.html'
    form_class = forms.VeiculoForm
    success_url = reverse_lazy('veiculo_list')
    permission_required = 'veiculos.add_veiculo'


class VeiculosDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Veiculo
    template_name = 'veiculo_detail.html'
    form_class = forms.VeiculoForm
    success_url = reverse_lazy('veiculo_list')
    permission_required = 'veiculos.view_veiculo'


class VeiculosUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Veiculo
    template_name = 'veiculo_update.html'
    form_class = forms.VeiculoForm
    success_url = reverse_lazy('veiculo_list')
    permission_required = 'veiculos.change_veiculo'


class VeiculosDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Veiculo
    template_name = 'veiculo_delete.html'
    success_url = reverse_lazy('veiculo_list')
    permission_required = 'veiculos.delete_veiculo'
