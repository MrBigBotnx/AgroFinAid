# Generated by Django 5.0.7 on 2024-10-30 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_financiamento_data_criacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financiamento',
            name='condicoes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financiamento',
            name='termos_reembolso',
            field=models.TextField(blank=True, null=True),
        ),
    ]
