# Generated by Django 5.1.1 on 2024-11-04 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_compra_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
