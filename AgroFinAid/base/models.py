from django.db import models

# Create your models here.
# base/models.py

from django.db import models
from django.contrib.auth.models import User

class Beneficiario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    idade = models.IntegerField()  # Campo para idade
    tipo_atividade = models.CharField(max_length=50)  # agrícola ou negócio
    historico_financiamentos = models.TextField(blank=True)

from django.db import models
from django.utils import timezone

from django.db import models

# models.py
class Financiamento(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('A', 'Aceito'),
        ('R', 'Recusado'),
    ]

    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    prazo = models.IntegerField(help_text="Prazo do financiamento em meses")  # Novo campo
    taxa_juros = models.DecimalField(max_digits=5, decimal_places=2, help_text="Taxa de juros ao mês (%)")  # Novo campo
    termos_reembolso = models.TextField(blank=True, null=True)
    condicoes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Financiamento de {self.valor} - Status: {self.get_status_display()}"

    def calcular_amortizacao(self):
        """
        Calcula e salva as parcelas de amortização com base no valor, prazo e taxa de juros.
        """
        saldo_devedor = self.valor
        amortizacao = saldo_devedor / self.prazo
        parcelas = []

        for i in range(1, self.prazo + 1):
            juros = saldo_devedor * (self.taxa_juros / 100)
            parcela_total = amortizacao + juros
            saldo_devedor -= amortizacao

            # Adiciona a parcela ao histórico de amortizações
            parcelas.append(Amortizacao(
                financiamento=self,
                data_pagamento=timezone.now() + timezone.timedelta(days=30 * i),
                valor_pagamento=parcela_total,
                saldo_devedor=saldo_devedor,
                historico_reembolsos=f"Parcela {i} - Juros: {juros:.2f} - Amortização: {amortizacao:.2f}"
            ))

        # Salva as parcelas no banco de dados
        Amortizacao.objects.bulk_create(parcelas)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Salva o financiamento
        self.calcular_amortizacao()  # Gera as parcelas após salvar

class Atividade(models.Model):
    financiamento = models.ForeignKey(Financiamento, on_delete=models.CASCADE, blank=True, null=True)
    descricao = models.TextField()
    insumos = models.TextField()
    ferramentas = models.TextField()
    recursos_necessarios = models.TextField()

class Amortizacao(models.Model):
    financiamento = models.ForeignKey(Financiamento, on_delete=models.CASCADE)
    data_pagamento = models.DateField()
    valor_pagamento = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_devedor = models.DecimalField(max_digits=10, decimal_places=2)
    historico_reembolsos = models.TextField()
