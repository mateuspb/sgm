from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'movimentacoes', views.MovimentacoesAPIView, basename='movimentacoes')

urlpatterns = [
    path('movimentacoes/list/', views.MovimentacoesListView.as_view(), name='movimentacao_list'),
    path('movimentacoes/create/', views.MovimentacoesCreateView.as_view(), name='movimentacao_create'),
    path('movimentacoes/<int:pk>/detail/', views.MovimentacoesDetailView.as_view(), name='movimentacao_detail'),
    path('movimentacoes/<int:pk>/update/', views.MovimentacoesUpdateView.as_view(), name='movimentacao_update'),
    path('movimentacoes/<int:pk>/delete/', views.MovimentacoesDeleteView.as_view(), name='movimentacao_delete'),

    path('api/v1/', include(router.urls)),
]
