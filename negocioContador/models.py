from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()

    def __str__(self):
        return f"Producto #{self.id} - Nombre: {self.nombre} - Precio: {self.precio}"

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Boleta(models.Model):
    fecha = models.DateField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, through='DetalleBoleta')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Boleta #{self.id} - Fecha: {self.fecha} - Total: {self.total}"
    

class BoletaProveedor(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, through='DetalleBoletaProveedor')

    def __str__(self):
        return f"BoletaProveedor #{self.id} - Proveedor: {self.proveedor.nombre} - Fecha: {self.fecha}"


class DetalleBoleta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()


class DetalleBoletaProveedor(models.Model):
    boleta_proveedor = models.ForeignKey(BoletaProveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    quien_entrego = models.CharField(max_length=100)
    quien_recibio = models.CharField(max_length=100)

    def __str__(self):
        return f"DetalleBoletaProveedor #{self.id} - BoletaProveedor: {self.boleta_proveedor.id} - Producto: {self.producto.nombre}"
