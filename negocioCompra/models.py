from django.db import models
from django.conf import settings
from django.utils import timezone


default_value = timezone.now()
# Create your models here.
class Proveedor(models.Model):
    RUT_PROVEEDOR = models.AutoField(primary_key=True)
    NOMBRE_PROVEEDOR = models.CharField(max_length=200)
    TELEFONO_PROVEEDOR = models.CharField(max_length=200)
    DIRECCION = models.CharField(max_length=200)

class Producto(models.Model): #crear los nuevos 
    ID_PRODUCTO = models.AutoField(primary_key=True)
    nombreProducto = models.CharField(max_length=100)
    precio = models.IntegerField(default=100)

def hrsDetail(self):
        return f"Salida #{self.id} - Fecha: {self.F_compra}"
        now = timezone.now()
        return current_date, current_time

class CompraNegocio(models.Model): 
    id_Compra= models.AutoField(primary_key=True)
    F_compra= models.DateTimeField(auto_now_add=True)
    hora = models.TimeField(default=hrsDetail)
    cantidad_total = models.PositiveIntegerField()
    Total_a_pagar=models.PositiveIntegerField()
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    proveedor=models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    
def str(self):
        return f"Salida #{self.id} - Fecha: {self.fecha}"

class Detalle_compra(models.Model):
    id_detalle= models.AutoField(primary_key=True) 
    fecha = models.DateTimeField(auto_now_add=True)
    compra_Negocio = models.ForeignKey(CompraNegocio, on_delete=models.CASCADE)


