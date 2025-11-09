from django.urls import path
from . import views


urlpatterns = [
    path('situacoes/list/', views.SituacoesListView.as_view(), name='situacao_list'),
    path('situacoes/create/', views.SituacoesCreateView.as_view(), name='situacao_create'),
    path('situacoes/<int:pk>/detail/', views.SituacoesDetailView.as_view(), name='situacao_detail'),
    path('situacoes/<int:pk>/update/', views.SituacoesUpdateView.as_view(), name='situacao_update'),
    path('situacoes/<int:pk>/delete/', views.SituacoesDeleteView.as_view(), name='situacao_delete'),
]
