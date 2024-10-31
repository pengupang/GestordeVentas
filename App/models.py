from django.db import models

# Create your models here.
class Proveedor(models.Model):
    Nombre = models.CharField (max_length=60)
    Representante = models.CharField (max_length=80)
    Contacto = models.CharField (max_length= 14)


class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    edad = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=[('Manager', 'Manager'), ('Empleado', 'Empleado')])

    