# Generated by Django 5.1.1 on 2024-11-14 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_reporte'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporte',
            name='detalles',
            field=models.TextField(blank=True, null=True),
        ),
    ]
