from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('negocioBodegas/', include('negocioBodegas.urls')),
    path('negocioCliente/', include('negocioCliente.urls')),
    path('negocioCompra/', include('negocioCompra.urls')),
    path('negocioContador/', include('negocioContador.urls')),
    path('negocioTransbanck/', include('negocioTransbanck.urls')),
    path('negocioVendedor/', include('negocioVendedor.urls')),
]