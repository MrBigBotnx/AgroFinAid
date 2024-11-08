# Generated by Django 5.0.7 on 2024-11-03 13:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_financiamento_condicoes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='financiamento',
            name='prazo',
            field=models.IntegerField(default=12, help_text='Prazo do financiamento em meses'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='financiamento',
            name='taxa_juros',
            field=models.DecimalField(decimal_places=2, default=12, help_text='Taxa de juros ao mês (%)', max_digits=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='atividade',
            name='financiamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.financiamento'),
        ),
    ]
