# base/admin.py
from django.contrib import admin
from .models import Beneficiario, Financiamento, Amortizacao

# Configuração para o modelo Beneficiario
@admin.register(Beneficiario)
class BeneficiarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'idade', 'tipo_atividade', 'usuario')
    search_fields = ('nome_completo', 'tipo_atividade')

# Configuração inline para o modelo Amortizacao
class AmortizacaoInline(admin.TabularInline):
    model = Amortizacao
    readonly_fields = ('data_pagamento', 'valor_pagamento', 'saldo_devedor', 'historico_reembolsos')
    can_delete = False
    extra = 0  # Define que não há linhas adicionais vazias por padrão

# Configuração para o modelo Financiamento
@admin.register(Financiamento)
class FinanciamentoAdmin(admin.ModelAdmin):
    inlines = [AmortizacaoInline]  # Adiciona a tabela de amortizações ao financiamento
    list_display = ('beneficiario', 'valor', 'prazo', 'taxa_juros', 'status', 'data_criacao')
    list_filter = ('status', 'data_criacao')
    actions = ['aprovar_financiamento', 'negar_financiamento']
    
    # Campos de leitura e edição no admin
    fields = ('beneficiario', 'valor', 'prazo', 'taxa_juros', 'status', 'data_criacao', 'termos_reembolso', 'condicoes')
    readonly_fields = ('data_criacao',)

    # Função para aprovar o financiamento
    def aprovar_financiamento(self, request, queryset):
        queryset.update(status='A')
        self.message_user(request, "Financiamentos aprovados com sucesso.")

    # Função para negar o financiamento
    def negar_financiamento(self, request, queryset):
        queryset.update(status='R')
        self.message_user(request, "Financiamentos negados com sucesso.")
