# Generated by Django 5.1 on 2024-11-08 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_merge_20241108_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='tipo',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Bodeguero', 'Bodeguero'), ('Vendedor', 'Vendedor')], max_length=10),
        ),
    ]
