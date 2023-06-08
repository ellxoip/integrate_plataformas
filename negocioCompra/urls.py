from django.contrib import admin
from django.urls import path
from .views import ProductoView
from .views import ComprarView
from .views import detailView

urlpatterns = [
    path('productos/', ProductoView.as_view(), name='producto_list'),
    path('productos/<int:id>', ProductoView.as_view(), name='producto_process'),
    path('ComprarFaltantes/', ComprarView.as_view(), name='ComprarFaltantes_list'),
    path('ComprarFaltantes/<int:id>', ComprarView.as_view(), name='ComprarFaltantes_process'),
    path('detalleCompra/', detailView.as_view(), name='detalleCompra_list'),
    path('detalleCompra/<int:id>', ComprarView.as_view(), name='detalleCompra_process')
]
