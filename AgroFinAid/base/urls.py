# base/urls.py

from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.landing_page, name='landing_page'),

    # Página de login (usando a view padrão do Django)
    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),

    # Pagina dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Página de logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Página de registro
    path('register/', views.register, name='register'),

    path('solicitar_financiamento/', views.solicitar_financiamento, name='solicitar_financiamento'),

      # URL para requisição AJAX de login
    path('ajax_login/', views.ajax_login, name='ajax_login'),
    path('ajax_finance_request/', views.solicitar_financiamento, name='ajax_finance_request'),
    path('ajax_register/', views.ajax_register, name='ajax_register'),

    path('ver_financiamento/<int:id>/', views.view_fund_request, name='view_fund_request'),

    path('editar_financiamento/<int:id>/', views.editar_financiamento, name='edit_fund_request'),

    path('relatorio/pdf/', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
   
    path('amortizacao/', views.amortizacao_geral, name='amortizacao_geral'),

    path('selecionar_financiamento/', views.selecionar_financiamento, name='selecionar_financiamento'),
    
    path('detalhes_financiamento/<int:financiamento_id>/', views.detalhes_financiamento, name='detalhes_financiamento'),

]
