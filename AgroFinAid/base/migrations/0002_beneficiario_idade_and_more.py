# Generated by Django 5.0.7 on 2024-10-29 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiario',
            name='idade',
            field=models.IntegerField(default=18),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='beneficiario',
            name='historico_financiamentos',
            field=models.TextField(blank=True),
        ),
    ]
