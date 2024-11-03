# Generated by Django 5.0.7 on 2024-10-30 01:32

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_financiamento_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='financiamento',
            name='data_criacao',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='financiamento',
            name='status',
            field=models.CharField(choices=[('P', 'Pendente'), ('A', 'Aceito'), ('R', 'Recusado')], default='P', max_length=1),
        ),
    ]
