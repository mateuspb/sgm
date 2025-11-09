from django.urls import path
from . import views


urlpatterns = [
    path('produtos/list/', views.ProdutosListView.as_view(), name='produto_list'),
    path('produtos/create/', views.ProdutosCreateView.as_view(), name='produto_create'),
    path('produtos/<int:pk>/detail/', views.ProdutosDetailView.as_view(), name='produto_detail'),
    path('produtos/<int:pk>/update/', views.ProdutosUpdateView.as_view(), name='produto_update'),
    path('produtos/<int:pk>/delete/', views.ProdutosDeleteView.as_view(), name='produto_delete'),
]
