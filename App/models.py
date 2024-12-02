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
    actualizado_por = models.CharField(max_length=100, null=True, blank=True)
    razon_actualizacion = models.TextField(null=True, blank=True)

    def precio_con_descuento(self):
        if self.descuento > 0:
            return self.precio * (1 - self.descuento / 100)
        return self.precio

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    fecha = models.DateField(null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, null=False, related_name='proveedor_compras')
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='producto_compras')
    habilitado = models.BooleanField(default=True)
    tipo = models.CharField(max_length=50, default='compra')

    def __str__(self):
        return f"{self.producto} - {self.proveedor.Nombre}"

    
class Venta(models.Model):
        fecha = models.DateField(auto_now_add=True)
        detalles = models.TextField()  # Información sobre los productos vendidos
        tipo = models.CharField(max_length=50, default='venta')
        producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Ejemplo: nombre del producto
        cantidad = models.IntegerField()  # Ejemplo: cantidad vendida
        precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Precio por unidad

        def total(self):
            """Método para calcular el total de la venta (cantidad * precio_unitario)."""
            return self.cantidad * self.precio_unitario


class Reporte(models.Model):
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    tipo_reporte = models.CharField(max_length=50)
    detalles = models.TextField(blank=True, null=True)
    compras = models.ManyToManyField(Compra, blank=True)
    ventas = models.ManyToManyField(Venta, blank=True)

    def __str__(self):
        return f"Reporte {self.id} - {self.tipo_reporte} ({self.fecha_inicio} a {self.fecha_final})"


class HistorialInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=[('entrada', 'Entrada'), ('salida', 'Salida')])
    fecha = models.DateTimeField(auto_now_add=True)
    detalle = models.TextField()

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} - {self.cantidad}"           
    
class SeleccionProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    seleccionado_en = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.producto.precio_con_descuento() * self.cantidad

    def aumentar_cantidad(self):
        self.cantidad += 1
        self.save()

    def disminuir_cantidad(self):
        if self.cantidad > 1:
            self.cantidad -= 1
            self.save()

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad}"
