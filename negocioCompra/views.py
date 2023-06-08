from django.http.response import JsonResponse
from django.shortcuts import render
from django.db.models import Sum
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.db.models import ProtectedError
from decimal import Decimal
from django.db.models import F
import json

from .models import Producto,CompraNegocio, Proveedor, Detalle_compra 

class ProductoView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            product = list(Producto.objects.filter(ID_PRODUCTO=id).values())
            if len(product) > 0:
                buy = product[0]
                datos = {'mensaje': "producto encontrado exitosamente", 'procucto': buy}
            else:
                datos = {'mensaje': "Producto no Encontrado Intente nuevamente..."}
            return JsonResponse(datos)
        else:
            product = list(Producto.objects.values())
            if len(product) > 0:
                datos = {'mensaje': "Productos encontrados exitosamente", 'producto': product}
            else:
                datos = {'mensaje': "Productos no Encontrados, Intente nuevamente..."}
            return JsonResponse(datos)
    
    def post(self, request):
        print(request.body)
        jd = json.loads(request.body)
        print(jd)
        Producto.objects.create(ID_PRODUCTO=jd['ID_PRODUCTO'], nombreProducto=jd['nombreProducto'])
        datos = {'mensaje': "Producto Agregado Correctamente"}
        return JsonResponse(datos)
    
    def put(self,request, id):
        jd = json.loads(request.body)
        productos=list(Producto.objects.filter(ID_PRODUCTO=id).values())
        if len(productos) > 0:
            producto=Producto.objects.get(ID_PRODUCTO=id)
            producto.nombreProducto=jd['nombreProducto']
            producto.precio=jd['precio']
            producto.save(),
            datos = {'mensaje': "Datos Modificados"}            
        else: 
            datos = {'mensaje': "producto no encontrado, intente nuevamente..."}
        return JsonResponse(datos)
    
    def delete(self,request,id):
        productos = list(Producto.objects.filter(ID_PRODUCTO=id).values())  
        if len(productos) > 0:
            Producto.objects.filter(ID_PRODUCTO=id).delete()
            datos = {'mensaje': "Producto Eliminado Correctamente"}
        else:
            datos = {'mensaje': "producto no encontrado, Intente nuevamente..."}
        return JsonResponse(datos)


  
  
class ComprarView(View): 

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            compra = list(CompraNegocio.objects.filter(id_Compra=id).values())
            if len(compra) > 0:
                buy = compra[0]
                datos = {'mensaje': "compra encontrada exitosamente", 'buy': buy}
            else:
                datos = {'mensaje': "compra no Encontrada Intente nuevamente..."}
            return JsonResponse(datos)
        else:
            compra = list(CompraNegocio.objects.values())
            if len(compra) > 0:
                datos = {'mensaje': "comprass encontradas exitosamente", 'compra': compra}
            else:
                datos = {'mensaje': "Compras no Encontradas Intente nuevamente..."}
            return JsonResponse(datos)
     
    def post(self, request):
        
        print(request.body)
        jd = json.loads(request.body)
        print(jd)
        suma = jd['cantidad_total']
        CompraNegocio.objects.update(cantidad_total=F('cantidad_total') + suma)

        producto = Producto.objects.get(ID_PRODUCTO=jd['ID_PRODUCTO'])
        precio_producto = producto.precio

        total_a_pagar = Decimal(precio_producto) * Decimal(suma)
        compra= CompraNegocio.objects.create(id_Compra=jd['id_Compra'], F_compra=jd['F_compra'], hora=jd['hora'], cantidad_total=jd['cantidad_total'], Total_a_pagar=total_a_pagar, producto_id=jd['ID_PRODUCTO'], proveedor_id=jd['RUT_PROVEEDOR'])
        registro = Detalle_compra(compra_Negocio=compra)
        registro.save()
        datos = {'mensaje': "Compra creada con exito"}
        return JsonResponse(datos)

        
    def put(self,request, id):
        jd = json.loads(request.body)
        buy=list(CompraNegocio.objects.filter(id_Compra=id).values())
        if len(buy) > 0:
            compra=CompraNegocio.objects.get(id_Compra=id)
            compra.F_compra=jd['F_compra']
            compra.hora=jd['hora']
            compra.cantidad_total=jd['cantidad_total']
            compra.producto_id=jd['ID_PRODUCTO']
            compra.proveedor_id=jd['RUT_PROVEEDOR']
            compra.save(),
            datos = {'mensaje': "Datos Modificados"}            
        else: 
            datos = {'mensaje': "productos no encontrados intente nuevamente..."}
        return JsonResponse(datos)
    
    def delete(self, request, id):
        try:
            compra = CompraNegocio.objects.get(id_Compra=id)
            compra.delete()
            datos = {'mensaje': "Compra Eliminada Correctamente"}
        except ProtectedError:
            datos = {'mensaje': "No se puede eliminar la compra, está asociada a otros objetos"}
        return JsonResponse(datos)


class detailView(View): 
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            detail = list(Detalle_compra.objects.filter(id_Compra=id).values())
            if len(detail) > 0:
                buy = detail[0]
                datos = {'mensaje': "Detalle encontrado exitosamente", 'detalle': buy}
            else:
                datos = {'mensaje': "Detalle no Encontrado, Intente nuevamente..."}
            return JsonResponse(datos)
        else:
            detail = list(Detalle_compra.objects.values())
            if len(detail) > 0:
                datos = {'mensaje': "Detalles encontrados exitosamente", 'compra': detail}
            else:
                datos = {'mensaje': "Detalless no Encontrados, Intente nuevamente..."}
            return JsonResponse(datos)
