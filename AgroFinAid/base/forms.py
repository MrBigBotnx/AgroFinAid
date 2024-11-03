from django import forms
from .models import Beneficiario, Financiamento, Atividade, Amortizacao

class BeneficiarioForm(forms.ModelForm):
    class Meta:
        model = Beneficiario
        fields = ['usuario', 'nome_completo', 'idade', 'tipo_atividade', 'historico_financiamentos']
        widgets = {
            'historico_financiamentos': forms.Textarea(attrs={'rows': 4}),
        }

class FinanciamentoForm(forms.ModelForm):
    class Meta:
        model = Financiamento
        fields = ['valor']


class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = ['financiamento', 'descricao', 'insumos', 'ferramentas', 'recursos_necessarios']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'insumos': forms.Textarea(attrs={'rows': 3}),
            'ferramentas': forms.Textarea(attrs={'rows': 3}),
            'recursos_necessarios': forms.Textarea(attrs={'rows': 3}),
        }

class AmortizacaoForm(forms.ModelForm):
    class Meta:
        model = Amortizacao
        fields = ['financiamento', 'data_pagamento', 'valor_pagamento', 'saldo_devedor', 'historico_reembolsos']
        widgets = {
            'historico_reembolsos': forms.Textarea(attrs={'rows': 3}),
        }
