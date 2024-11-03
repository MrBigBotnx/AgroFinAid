# Generated by Django 5.0.7 on 2024-10-29 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_beneficiario_idade_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='financiamento',
            name='status',
            field=models.CharField(choices=[('P', 'Pendente'), ('A', 'Aceite'), ('R', 'Recusado')], default='P', max_length=1),
        ),
    ]
