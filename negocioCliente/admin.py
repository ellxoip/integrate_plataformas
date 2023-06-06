from django.contrib import admin
from .models import Cliente, Producto, CarritoDeCompras, ItemCarrito, Region, Comuna

admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(CarritoDeCompras)
admin.site.register(ItemCarrito)
admin.site.register(Region)
admin.site.register(Comuna)