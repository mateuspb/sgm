from django.urls import path
from . import views


urlpatterns = [
    path('tiposcargas/list/', views.TiposcargasListView.as_view(), name='tipocarga_list'),
    path('tiposcargas/create/', views.TiposcargasCreateView.as_view(), name='tipocarga_create'),
    path('tiposcargas/<int:pk>/detail/', views.TiposcargasDetailView.as_view(), name='tipocarga_detail'),
    path('tiposcargas/<int:pk>/update/', views.TiposcargasUpdateView.as_view(), name='tipocarga_update'),
    path('tiposcargas/<int:pk>/delete/', views.TiposcargasDeleteView.as_view(), name='tipocarga_delete'),
]
