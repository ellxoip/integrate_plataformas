from django.contrib import admin
from django.urls import path

from django.urls import path
from .views import crear_boleta, crear_producto, crear_boleta_proveedor, obtener_boletas, obtener_boleta, obtener_boleta_proveedor, obtener_boletas_proveedores, eliminar_boleta, eliminar_boleta_proveedor, crear_proveedor

urlpatterns = [
    path('crear_boleta/', crear_boleta, name='crear_boleta'),
    path('crear_boleta_proveedor/', crear_boleta_proveedor, name='crear_boleta_proveedor'),
    path('obtener_boleta/<int:boleta_id>/', obtener_boleta, name='obtener_boleta'),
    path('obtener_boletas/', obtener_boletas, name='obtener_boletas'),
    path('obtener_boleta_proveedor/<int:boleta_id>/', obtener_boleta_proveedor, name='obtener_boleta_proveedor'),
    path('obtener_boletas_proveedores/', obtener_boletas_proveedores, name='obtener_boletas_proveedores'),
    path('eliminar_boleta/<int:boleta_id>/', eliminar_boleta, name='eliminar_boleta'),
    path('eliminar_boleta_proveedor/<int:boleta_id>/', eliminar_boleta_proveedor, name='eliminar_boleta_proveedor'),
    path('crear_producto/', crear_producto, name='crear_producto'),
    path('crear_proveedor/', crear_proveedor, name='crear_proveedor'),
]
