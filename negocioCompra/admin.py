from django.contrib import admin
from .models import CompraNegocio, Detalle_compra, Producto, Proveedor

# Register your models here.
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Detalle_compra)
admin.site.register(CompraNegocio)
