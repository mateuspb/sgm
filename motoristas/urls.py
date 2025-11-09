from django.urls import path
from . import views


urlpatterns = [
    path('motoristas/list/', views.MotoristasListView.as_view(), name='motorista_list'),
    path('motoristas/create/', views.MotoristasCreateView.as_view(), name='motorista_create'),
    path('motoristas/<int:pk>/detail/', views.MotoristasDetailView.as_view(), name='motorista_detail'),
    path('motoristas/<int:pk>/update/', views.MotoristasUpdateView.as_view(), name='motorista_update'),
    path('motoristas/<int:pk>/delete/', views.MotoristasDeleteView.as_view(), name='motorista_delete'),
]
