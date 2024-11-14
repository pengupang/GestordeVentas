from django.db import models

# Create your models here.
class Proveedor(models.Model):
    Nombre = models.CharField (max_length=60,null=False)
    Representante = models.CharField (max_length=80)
    Contacto = models.CharField (max_length= 14)
    habilitado = models.BooleanField(default=True)

    def __str__(self):
        return self.Nombre

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    edad = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=[('Manager', 'Manager'), ('Bodeguero', 'Bodeguero'),('Vendedor', 'Vendedor')])
    habilitado = models.BooleanField(default=True)

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    cantidad = models.IntegerField(default=0)
    precio = models.IntegerField()
    habilitado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to="imgProducts/")
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Porcentaje de descuento, e.g., 10.0 para 10%

    def precio_con_descuento(self):
        if self.descuento > 0:
            return self.precio * (1 - self.descuento / 100)
        return self.precio

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT,null= False, related_name='proveedor_compras')
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    producto= models.ForeignKey(Producto,on_delete=models.PROTECT, related_name='producto_compras') 
    habilitado = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.producto} - {self.proveedor.Nombre}"
    