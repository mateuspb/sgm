from django.urls import path
from . import views


urlpatterns = [
    path('veiculos/list/', views.VeiculosListView.as_view(), name='veiculo_list'),
    path('veiculos/create/', views.VeiculosCreateView.as_view(), name='veiculo_create'),
    path('veiculos/<int:pk>/detail/', views.VeiculosDetailView.as_view(), name='veiculo_detail'),
    path('veiculos/<int:pk>/update/', views.VeiculosUpdateView.as_view(), name='veiculo_update'),
    path('veiculos/<int:pk>/delete/', views.VeiculosDeleteView.as_view(), name='veiculo_delete'),
]
