# Generated by Django 5.1 on 2024-11-04 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_empleado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto', models.CharField(max_length=50)),
                ('cantidad', models.IntegerField()),
                ('precio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('cantidad', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('habilitado', models.BooleanField(default=True)),
            ],
        ),
    ]
