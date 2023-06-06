from django.urls import path
from . import views

urlpatterns = [
    path('registro_provincia/', views.registro_provincia, name='registro_provincia'),
    path('registro_region/', views.registro_region, name='registro_region'),
    path('registro_comuna/', views.registro_comuna, name='registro_comuna'),
    path('registro_cliente/', views.registro_cliente, name='registro_cliente'),
    path('registro_cliente/<int:cliente_id>/', views.registro_cliente, name='registro_cliente'),
    path('crear_productos/', views.crear_producto, name='crear_producto'),
    path('listar_productos/', views.listar_productos, name='listar_productos'),
    path('productos/', views.listar_productos, name='listar_productos'),
    path('comprar_producto/', views.comprar_producto, name='comprar_producto'),
    path('visualizar_carrito/', views.visualizar_carrito, name='visualizar_carrito'),
    path('seleccionar_retiro_tienda/', views.seleccionar_retiro_tienda, name='seleccionar_retiro_tienda'),
]