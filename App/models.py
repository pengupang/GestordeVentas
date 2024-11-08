from django.db import models

# Create your models here.
class Proveedor(models.Model):
    Nombre = models.CharField (max_length=60)
    Representante = models.CharField (max_length=80)
    Contacto = models.CharField (max_length= 14)
    habilitado = models.BooleanField(default=True)


class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    edad = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=[('Manager', 'Manager'), ('Empleado', 'Empleado')])
    habilitado = models.BooleanField(default=True)

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    habilitado = models.BooleanField(default=True)

class Compra(models.Model):
    producto = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    
