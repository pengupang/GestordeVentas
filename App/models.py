from django.db import models

# Create your models here.
class Proveedor(models.Model):
    Nombre = models.CharField (max_length=60)
    Representante = models.CharField (max_length=80)
    Contacto = models.CharField (max_length= 14)
