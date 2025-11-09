from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from . import models, forms


class ProdutosListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Produto
    template_name = 'produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 10
    permission_required = 'produtos.view_produto'

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)

        return queryset


class ProdutosCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Produto
    template_name = 'produto_create.html'
    form_class = forms.ProdutoForm
    success_url = reverse_lazy('produto_list')
    permission_required = 'produtos.add_produto'


class ProdutosDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Produto
    template_name = 'produto_detail.html'
    form_class = forms.ProdutoForm
    success_url = reverse_lazy('produto_list')
    permission_required = 'produtos.view_produto'


class ProdutosUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Produto
    template_name = 'produto_update.html'
    form_class = forms.ProdutoForm
    success_url = reverse_lazy('produto_list')
    permission_required = 'produtos.change_produto'


class ProdutosDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Produto
    template_name = 'produto_delete.html'
    success_url = reverse_lazy('produto_list')
    permission_required = 'produtos.delete_produto'
