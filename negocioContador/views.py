import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Boleta, DetalleBoleta, Producto, Proveedor, DetalleBoletaProveedor, BoletaProveedor
from django.shortcuts import get_object_or_404
# Create your views here.


@csrf_exempt
def crear_boleta(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        productos = data['productos']
        total = 0.0

        boleta = Boleta.objects.create()

        for producto in productos:
            producto_id = producto['id']
            cantidad = producto['cantidad']

            try:
                producto_obj = Producto.objects.get(id=producto_id)
                precio = producto_obj.precio
                subtotal = float(precio) * cantidad
                total += subtotal

                detalle = DetalleBoleta.objects.create(boleta=boleta, producto=producto_obj, cantidad=cantidad)
            except Producto.DoesNotExist:
                return JsonResponse({'error': 'El producto con el ID {} no existe'.format(producto_id)}, status=400)

        boleta.total = total
        boleta.save()

        detalles = DetalleBoleta.objects.filter(boleta=boleta)

        boleta_data = {
            'id': boleta.id,
            'fecha': boleta.fecha,
            'total': str(boleta.total),
            'productos': []
        }

        for detalle in detalles:
            producto_data = {
                'id': detalle.producto.id,
                'nombre': detalle.producto.nombre,
                'precio': str(detalle.producto.precio),
                'cantidad': detalle.cantidad
            }
            boleta_data['productos'].append(producto_data)

        return JsonResponse(boleta_data)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def crear_boleta_proveedor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        productos = data['productos']
        total = 0.0

        proveedor_id = data['proveedor_id']
        proveedor_obj = Proveedor.objects.get(id=proveedor_id)

        boleta_proveedor = BoletaProveedor.objects.create(proveedor=proveedor_obj)

        for producto in productos:
            producto_id = producto['id']
            cantidad = producto['cantidad']
            quien_entrego = producto['quien_entrego']
            quien_recibio = producto['quien_recibio']

            try:
                producto_obj = Producto.objects.get(id=producto_id)
                precio = producto_obj.precio
                subtotal = float(precio) * cantidad
                total += subtotal

                detalle = DetalleBoletaProveedor.objects.create(boleta_proveedor=boleta_proveedor, producto=producto_obj, cantidad=cantidad, quien_entrego=quien_entrego, quien_recibio=quien_recibio)
            except Producto.DoesNotExist:
                return JsonResponse({'error': 'El producto con el ID {} no existe'.format(producto_id)}, status=400)

        boleta_proveedor.precio_total = total
        boleta_proveedor.save()

        detalles = DetalleBoletaProveedor.objects.filter(boleta_proveedor=boleta_proveedor)

        boleta_data = {
            'id': boleta_proveedor.id,
            'proveedor': boleta_proveedor.proveedor.nombre,
            'fecha': boleta_proveedor.fecha,
            'productos': []
        }

        for detalle in detalles:
            producto_data = {
                'id': detalle.producto.id,
                'nombre': detalle.producto.nombre,
                'precio': str(detalle.producto.precio),
                'cantidad': detalle.cantidad,
                'quien_entrego': detalle.quien_entrego,
                'quien_recibio': detalle.quien_recibio
            }
            boleta_data['productos'].append(producto_data)

        return JsonResponse(boleta_data)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)



@csrf_exempt
def obtener_boleta(request, boleta_id):
    if request.method == 'GET':
        try:
            boleta = Boleta.objects.get(id=boleta_id)
            detalles = DetalleBoleta.objects.filter(boleta=boleta)

            boleta_data = {
                'id': boleta.id,
                'fecha': boleta.fecha,
                'productos': [],
                'total': 0.0
            }

            for detalle in detalles:
                producto_data = {
                    'id': detalle.producto.id,
                    'nombre': detalle.producto.nombre,
                    'precio': str(detalle.producto.precio),
                    'cantidad': detalle.cantidad
                }
                boleta_data['productos'].append(producto_data)

                subtotal = detalle.producto.precio * detalle.cantidad
                boleta_data['total'] += subtotal

            boleta_data['total'] = format(boleta_data['total'], '.2f')

            return JsonResponse(boleta_data)
        except Boleta.DoesNotExist:
            return JsonResponse({'error': 'La boleta con el ID {} no existe'.format(boleta_id)}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    


@csrf_exempt
def obtener_boletas(request):
    if request.method == 'GET':
        boletas = Boleta.objects.all()
        boletas_data = []

        if boletas:
            for boleta in boletas:
                detalles = DetalleBoleta.objects.filter(boleta=boleta)

                boleta_data = {
                    'id': boleta.id,
                    'fecha': boleta.fecha,
                    'total': str(boleta.total),
                    'productos': []
                }

                for detalle in detalles:
                    producto_data = {
                        'id': detalle.producto.id,
                        'nombre': detalle.producto.nombre,
                        'precio': str(detalle.producto.precio),
                        'cantidad': detalle.cantidad
                    }
                    boleta_data['productos'].append(producto_data)

                boletas_data.append(boleta_data)
        else:
            return JsonResponse({'error': 'No hay boletas registradas'})

        return JsonResponse(boletas_data, safe=False)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def obtener_boleta_proveedor(request, boleta_id):
    if request.method == 'GET':
        try:
            boleta = BoletaProveedor.objects.get(id=boleta_id)
            detalles = DetalleBoletaProveedor.objects.filter(boleta_proveedor=boleta)

            boleta_data = {
                'id': boleta.id,
                'fecha': boleta.fecha,
                'proveedor': boleta.proveedor.nombre,
                'productos': [],
                'total': 0.0,  # Agregar campo para el total inicializado en 0.0
                'quienes_entregaron': [],
                'quienes_recibieron': []
            }

            for detalle in detalles:
                producto_data = {
                    'id': detalle.producto.id,
                    'nombre': detalle.producto.nombre,
                    'precio': str(detalle.producto.precio),
                    'cantidad': detalle.cantidad
                }
                boleta_data['productos'].append(producto_data)
                boleta_data['quienes_entregaron'].append(detalle.quien_entrego)
                boleta_data['quienes_recibieron'].append(detalle.quien_recibio)

                # Calcular subtotal y sumarlo al total
                subtotal = detalle.producto.precio * detalle.cantidad
                boleta_data['total'] += subtotal

            boleta_data['total'] = str(boleta_data['total'])  # Convertir el total a string

            return JsonResponse(boleta_data)
        except BoletaProveedor.DoesNotExist:
            return JsonResponse({'error': 'La boleta con el ID {} no existe'.format(boleta_id)}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)



@csrf_exempt
def obtener_boletas_proveedores(request):
    if request.method == 'GET':
        try:
            boletas = BoletaProveedor.objects.all()
            boletas_data = []

            for boleta in boletas:
                detalles = DetalleBoletaProveedor.objects.filter(boleta_proveedor=boleta)
                boleta_data = {
                    'id': boleta.id,
                    'fecha': boleta.fecha,
                    'proveedor': boleta.proveedor.nombre,
                    'productos': [],
                    'total': 0.0,
                    'quienes_entregaron': [],
                    'quienes_recibieron': []
                }

                for detalle in detalles:
                    producto_data = {
                        'id': detalle.producto.id,
                        'nombre': detalle.producto.nombre,
                        'precio': str(detalle.producto.precio),
                        'cantidad': detalle.cantidad
                    }
                    boleta_data['productos'].append(producto_data)
                    boleta_data['quienes_entregaron'].append(detalle.quien_entrego)
                    boleta_data['quienes_recibieron'].append(detalle.quien_recibio)

                    subtotal = detalle.producto.precio * detalle.cantidad
                    boleta_data['total'] += subtotal

                boleta_data['total'] = str(boleta_data['total'])
                boletas_data.append(boleta_data)

            if len(boletas_data) > 0:
                return JsonResponse(boletas_data, safe=False)
            else:
                return JsonResponse({'error': 'No hay boletas registradas'}, status=404)
        except BoletaProveedor.DoesNotExist:
            return JsonResponse({'error': 'No se encontraron boletas'}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)



@csrf_exempt
def eliminar_boleta(request, boleta_id):
    if request.method == 'DELETE':
        try:
            boleta = Boleta.objects.get(id=boleta_id)
            boleta.delete()
            return JsonResponse({'mensaje': 'Boleta eliminada exitosamente'})
        except Boleta.DoesNotExist:
            return JsonResponse({'error': 'La boleta con el ID {} no existe'.format(boleta_id)}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def eliminar_boleta_proveedor(request, boleta_id):
    if request.method == 'DELETE':
        try:
            boleta = BoletaProveedor.objects.get(id=boleta_id)
            boleta.delete()
            return JsonResponse({'message': 'Boleta eliminada exitosamente'})
        except BoletaProveedor.DoesNotExist:
            return JsonResponse({'error': 'La boleta con el ID {} no existe'.format(boleta_id)}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def crear_producto(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        precio = data.get('precio')

        if not nombre or not precio:
            return JsonResponse({'error': 'Nombre y precio son campos requeridos'}, status=400)

        producto = Producto.objects.create(nombre=nombre, precio=precio)

        return JsonResponse({'mensaje': 'Producto creado exitosamente'})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    

@csrf_exempt
def crear_proveedor(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        nombre = data.get('nombre')
        direccion = data.get('direccion')

        # Validar datos requeridos
        if not nombre or not direccion:
            return JsonResponse({'error': 'Se requiere nombre y dirección del proveedor'}, status=400)

        proveedor = Proveedor(nombre=nombre, direccion=direccion)
        proveedor.save()

        proveedor_data = {
            'id': proveedor.id,
            'nombre': proveedor.nombre,
            'direccion': proveedor.direccion
        }

        return JsonResponse(proveedor_data, status=201)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    


    

