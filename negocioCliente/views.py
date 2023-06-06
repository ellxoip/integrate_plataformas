from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from .models import Provincia, Region, Comuna, Producto, CarritoDeCompras, ItemCarrito, Cliente, Vendedor 


@csrf_exempt
def registro_provincia(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')

        if not nombre:
            return JsonResponse({'error': 'Falta algún campo'}, status=400)

        provincia = Provincia(nombre=nombre)
        provincia.save()

        return JsonResponse({'mensaje': 'Provincia registrada exitosamente', 'provincia_id': provincia.id})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def registro_region(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')

        if not nombre:
            return JsonResponse({'error': 'Falta algún campo'}, status=400)

        region = Region(nombre=nombre)
        region.save()

        return JsonResponse({'mensaje': 'Región registrada exitosamente', 'region_id': region.id}, status=201)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def registro_comuna(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        region_id = data.get('region_id')

        if not all([nombre, region_id]):
            return JsonResponse({'error': 'Falta algún campo'}, status=400)

        region = get_object_or_404(Region, id=region_id)

        comuna = Comuna(nombre=nombre, region=region)
        comuna.save()

        return JsonResponse({'mensaje': 'Comuna registrada exitosamente', 'comuna_id': comuna.id})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def registro_cliente(request, cliente_id=None):
    if request.method == 'GET':
        if cliente_id:
            cliente = get_object_or_404(Cliente, id=cliente_id)
            return JsonResponse({'cliente': model_to_dict(cliente)})
        else:
            clientes = list(Cliente.objects.values())
            return JsonResponse({'clientes': clientes})

    elif request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        direccion = data.get('direccion')
        correo_electronico = data.get('correo_electronico')
        comuna_id = data.get('comuna_id')

        if not all([nombre, apellido, direccion, correo_electronico, comuna_id]):
            return JsonResponse({'error': 'Falta algún campo'}, status=400)

        comuna = get_object_or_404(Comuna, id=comuna_id)

        cliente = Cliente(nombre=nombre, apellido=apellido, direccion=direccion, correo_electronico=correo_electronico, comuna=comuna)
        cliente.save()

        return JsonResponse({'mensaje': 'Cliente registrado exitosamente', 'cliente_id': cliente.id})

    elif request.method == 'PUT':
        if not cliente_id:
            return JsonResponse({'error': 'Se necesita el id del cliente'}, status=400)

        cliente = get_object_or_404(Cliente, id=cliente_id)
        data = json.loads(request.body)

        cliente.nombre = data.get('nombre', cliente.nombre)
        cliente.apellido = data.get('apellido', cliente.apellido)
        cliente.direccion = data.get('direccion', cliente.direccion)
        cliente.correo_electronico = data.get('correo_electronico', cliente.correo_electronico)
        comuna_id = data.get('comuna_id', cliente.comuna_id)

        cliente.save()

        return JsonResponse({'mensaje': 'Cliente actualizado exitosamente'})

    elif request.method == 'DELETE':
        if not cliente_id:
            return JsonResponse({'error': 'Se necesita el id del cliente'}, status=400)

        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente.delete()

        return JsonResponse({'mensaje': 'Cliente eliminado exitosamente'})

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)



@csrf_exempt
def crear_producto(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        precio = data.get('precio')

        if not all([nombre, precio]):
            return JsonResponse({'error': 'Falta algún campo'}, status=400)

        producto = Producto(nombre=nombre, precio=precio)
        producto.save()

        return JsonResponse({'mensaje': 'Producto creado exitosamente', 'producto_id': producto.id})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def listar_productos(request):
    productos = Producto.objects.all()
    data = {
        'productos': list(productos.values())
    }
    return JsonResponse(data)


@csrf_exempt
def comprar_producto(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cliente_id = data.get('cliente_id')
        producto_id = data.get('producto_id')
        cantidad = data.get('cantidad')

        if not all([cliente_id, producto_id, cantidad]):
            return JsonResponse({'error': 'Falta algún campo'}, status=400)

        if cantidad <= 0:
            return JsonResponse({'error': 'La cantidad debe ser mayor a cero'}, status=400)

        # Aquí puedes agregar la lógica adicional, como obtener el cliente, vendedor, etc.

        # Ejemplo:
        cliente = get_object_or_404(Cliente, id=cliente_id)
        producto = get_object_or_404(Producto, id=producto_id)

        carrito, _ = CarritoDeCompras.objects.get_or_create(cliente=cliente)
        item, _ = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
        item.cantidad += cantidad
        item.save()

        return JsonResponse({'mensaje': 'Producto agregado al carrito exitosamente'})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def crear_vendedor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        telefono = data.get('telefono')

        if not all([nombre, apellido, telefono]):
            return JsonResponse({'error': 'Falta algún campo'}, status=400)

        vendedor = Vendedor( nombre=nombre, apellido=apellido, telefono=telefono)
        vendedor.save()

        return JsonResponse({'mensaje': 'Vendedor creado exitosamente', 'vendedor_id': vendedor.id})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def visualizar_carrito(request):
    if request.method == 'GET':
        carrito = CarritoDeCompras.objects.first()  # Obtén el primer carrito de compras disponible (puedes ajustar esto según tus necesidades)

        if not carrito:
            return JsonResponse({'mensaje': 'No hay carritos de compras disponibles'})

        items = ItemCarrito.objects.filter(carrito=carrito)

        productos = []
        for item in items:
            producto = item.producto
            cantidad = item.cantidad
            productos.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': str(producto.precio),
                'cantidad': cantidad
            })

        return JsonResponse({'productos': productos})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
@csrf_exempt
def seleccionar_retiro_tienda(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cliente_id = data.get('cliente_id')
        vendedor_id = data.get('vendedor_id')
        retiro_en_tienda = data.get('retiro_en_tienda')

        if cliente_id is None or vendedor_id is None or retiro_en_tienda is None:
            return JsonResponse({'error': 'Falta algún campo'}, status=400)

        if not isinstance(retiro_en_tienda, bool):
            return JsonResponse({'error': 'El campo retiro_en_tienda debe ser un booleano'}, status=400)

        carrito = get_object_or_404(CarritoDeCompras, cliente__id=cliente_id)
        vendedor = get_object_or_404(Vendedor, id=vendedor_id)

        carrito.retiro_en_tienda = retiro_en_tienda
        carrito.vendedor = vendedor
        carrito.save()

        return JsonResponse({'mensaje': 'Opción de retiro en tienda seleccionada correctamente', 'nombre_vendedor': vendedor.nombre_vendedor})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)