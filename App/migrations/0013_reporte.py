# Generated by Django 5.1.1 on 2024-11-14 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0012_compra_fecha'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_generacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_inicio', models.DateField()),
                ('fecha_final', models.DateField()),
                ('tipo_reporte', models.CharField(max_length=50)),
                ('compras', models.ManyToManyField(blank=True, to='App.compra')),
                ('ventas', models.ManyToManyField(blank=True, to='App.venta')),
            ],
        ),
    ]
