# Generated by Django 5.1 on 2024-11-13 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_alter_empleado_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(default=1, upload_to='imgProducts/'),
            preserve_default=False,
        ),
    ]
