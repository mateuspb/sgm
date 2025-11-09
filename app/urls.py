from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

from movimentacoes.views import gerar_pdf, salvar_assinatura


urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('api/v1/', include('authentication.urls')),

    path('', views.home, name='home'),

    path('', include('clientes.urls')),
    path('', include('motoristas.urls')),
    path('', include('movimentacoes.urls')),
    path('', include('produtos.urls')),
    path('', include('situacoes.urls')),
    path('', include('tiposcargas.urls')),
    path('', include('veiculos.urls')),

    # Assinatura do Documento
    path('ajax/salvar-assinatura/', salvar_assinatura, name='salvar-assinatura'),

    # Geração do PDF
    path('ajax/gerar-pdf/<int:id>/', gerar_pdf, name='gerar-pdf'),
]
