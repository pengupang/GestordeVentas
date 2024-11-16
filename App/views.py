from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from App.models import Proveedor, Empleado, Compra,Producto,Venta, Reporte, HistorialInventario
from .forms import ProveedorForm, EmpleadoForm, CompraForm,ProductoForm



# Create your views here.
def login (request):
    return render(request,'login.html')

def inicio (request):
    return render(request,'inicio.html')

"""
View Empleados 
"""
def empleados (request):
    empleado = Empleado.objects.filter(habilitado=True)
    return render(request, 'empleados_ver.html', {'empleado': empleado})


def agregar_empleado(request):
    form = EmpleadoForm()
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado Ingresado') #Mensaje de empleado ingresado
            return redirect('../empleados_ver/') 
        else:
            messages.error(request, 'Error empleado no ingresado') # Mensaje de error
    data = {'form': form }
    return render(request,'empleados_agregar.html',data)

def deshabilitar_empleado(request, empleado_id):
    empleados = get_object_or_404(Empleado, id=empleado_id)
    empleados.habilitado = False  
    empleados.save()
    messages.success(request, f'Empleado {empleados.nombre} deshabilitado.')
    return redirect('empleados_ver')
    

"""
View Catalago 
"""
def catalogo_view(request):
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query, habilitado=True)
    else:
        productos = Producto.objects.filter(habilitado=True)
    
    return render(request, 'catalogo.html', {'productos': productos})

def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    carrito[producto_id] = carrito.get(producto_id, 0) + 1  # Incrementa la cantidad del producto
    request.session['carrito'] = carrito
    return redirect('carrito')  # Redirige al carrito después de agregar

def disminuir_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    if producto_id in carrito:
        if carrito[producto_id] > 1:
            carrito[producto_id] -= 1  # Disminuye la cantidad del producto
        else:
            del carrito[producto_id]  # Elimina el producto si la cantidad es 0
    request.session['carrito'] = carrito
    return redirect('carrito')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})  # Suponiendo que el carrito se guarda en la sesión
    productos_carrito = []

    # Recolecta productos en el carrito
    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.get(id=producto_id)
        precio_final = producto.precio_con_descuento()
        productos_carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'precio_unitario': producto.precio,
            'precio_final': precio_final,
            'descuento': producto.descuento,
        })

    # Calcular el total del carrito
    total = sum(item['precio_final'] * item['cantidad'] for item in productos_carrito)

    return render(request, 'carrito.html', {'productos_carrito': productos_carrito, 'total': total})

def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
    
    request.session['carrito'] = carrito
    return redirect('ver_carrito')

"""
View Inventario 
"""

def inventario_ver(request):
    productos = Producto.objects.filter(habilitado=True)
    return render(request, 'inventario_ver.html', {'productos': productos})

def actualizar_inventario(request, id):
    producto = get_object_or_404(Producto, id=id)
    form = ProductoForm(instance=producto)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.actualizado_por = request.user.username  # Registrar el usuario que hizo el cambio
            producto.razon_actualizacion = form.cleaned_data['razon_actualizacion']  # Registrar la razón
            producto.save()
            messages.success(request, 'Inventario actualizado correctamente.')
            return redirect('inventario_ver')
        else:
            messages.error(request, 'Error al actualizar el inventario.')

    return render(request, 'producto_actualizar.html', {'form': form, 'producto': producto})

def historial_inventario(request):
    # Obtener todo el historial (entradas y salidas)
    historial = HistorialInventario.objects.all().order_by('-fecha')  # Ordenar por fecha descendente
    return render(request, 'historial_inventario.html', {'historial': historial})

def agregar_producto(request):
    form = ProductoForm()
    if request.method == 'POST':
        form = ProductoForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto Ingresado') # Mensaje de producto ingresado
            return redirect('../inventario_ver/') 
        else:
            messages.error(request, 'Error producto no ingresado') # Mensaje de error
    data = {'form': form }
    return render(request,'producto_agregar.html',data)

def deshabilitar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.habilitado = False
    producto.save()
    messages.success(request, f'Producto {producto.nombre} deshabilitado.')
    return redirect('inventario_ver') 

def reducir_cantidad_producto(request, producto_id, cantidad):
    """
    Reduce la cantidad de un producto en el inventario.
    """
    producto = get_object_or_404(Producto, id=producto_id)
    
    if cantidad > producto.cantidad:
        messages.error(request, f"La cantidad a reducir ({cantidad}) excede el stock disponible ({producto.cantidad}).")
        return JsonResponse({'error': 'Cantidad excede el stock disponible'}, status=400)

    producto.cantidad -= cantidad
    producto.save()
    
    messages.success(request, f"Se redujeron {cantidad} unidades del producto '{producto.nombre}'.")
    return JsonResponse({'message': 'Cantidad reducida exitosamente', 'nueva_cantidad': producto.cantidad})
"""
View Proveedores 
"""
def proveedores_ingresar(request):
    form = ProveedorForm()
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Proveedor Ingresado')
            return redirect('../proveedor_ver/')
        else:
            messages.error(request,'Error proveedor no ingresado') # Mensaje el cual saldra cuando se meta un Proovedor
    data = {'form': form }
    return render(request,'proveedores_ingresar.html',data)

def proveedores_ver(request):
    proveedor = Proveedor.objects.all()
    data = {'proveedor':proveedor}
    return render(request,'proveedores_ver.html',data)

def deshabilitar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    proveedor.habilitado = False  
    proveedor.save()
    messages.success(request, f'Proveedor {proveedor.Nombre} deshabilitado.')
    return redirect('lista_proveedores')

def actualizar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor Actualizado')
            return redirect('lista_proveedores')  # Redirige a la lista de proveedores después de actualizar
    else:
        form = ProveedorForm(instance=proveedor)
    
    return render(request, 'actualizar_proveedor.html', {'form': form, 'proveedor': proveedor})

"""
View Compras 
"""
def compra_agregar(request):
    last_compra = Compra.objects.order_by('id').last()
    next_id = last_compra.id + 1 if last_compra else 1

    if request.method == "POST":
        if last_compra and next_id == Compra.objects.order_by('id').last().id:
            next_id += 1
        form = CompraForm(request.POST)
        if form.is_valid():
            form.instance.orden = next_id
            form.save() 
            messages.success(request, 'Producto agregado.') # Mensaje de producto agregado
            return redirect('compras_ver')

    form = CompraForm()

    productos = Producto.objects.all()

    context = {
        'form': form,
        'titulo': 'Agregar Compra',
        'productos': productos,
        'next_id': next_id,
    }
    return render(request, 'inventario_compras.html', context)


def compras_Ver (request):
    compras = Compra.objects.filter(habilitado=True)
    data = {'compra':compras}
    return render(request,'compras_ver.html',data)

def compra_deshabilitar(request,compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    compra.habilitado = False
    compra.save()
    messages.success(request, f'Producto {compra.producto} deshabilitado.')
    return redirect('compras_ver') 

def compra_editar(request,id):
    compra=Compra.objects.get(id=id)
    form=CompraForm(instance=compra)
    if request.method=="POST":
        form=CompraForm(request.POST,instance=compra)
        if form.is_valid():
            form.save()
        return compras_Ver(request)
    data={'form':form,'titulo':'Actualizar Compra'}
    return render(request,'inventario_compras.html',data)

"""
View Reportes
"""


def generar_reporte(request):
    reportes = []

    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_final = request.POST.get('fecha_final')
        tipo_reporte = request.POST.get('tipo_reporte')

        # Filtrar las compras y ventas según las fechas
        if tipo_reporte == 'compra':
            reportes = Compra.objects.filter(fecha__range=[fecha_inicio, fecha_final])
        elif tipo_reporte == 'venta':
            reportes = Venta.objects.filter(fecha__range=[fecha_inicio, fecha_final])
        elif tipo_reporte == 'ambos':
            reportes = list(Compra.objects.filter(fecha__range=[fecha_inicio, fecha_final])) + list(Venta.objects.filter(fecha__range=[fecha_inicio, fecha_final]))

        # Guardar los resultados en la sesión
        request.session['reportes'] = [reporte.id for reporte in reportes]

    else:
        # Recuperar los resultados de la sesión
        if 'reportes' in request.session:
            reportes_ids = request.session['reportes']
            reportes_compras = Compra.objects.filter(id__in=reportes_ids)
            reportes_ventas = Venta.objects.filter(id__in=reportes_ids)
            reportes = list(reportes_compras) + list(reportes_ventas)

    return render(request, 'reportes.html', {'reportes': reportes})










#def eliminar_proveedor(request, id):
#    proveedor = get_object_or_404(Proveedor, id = id)
#    if request.method == 'POST':
#        proveedor.delete()
#        messages.success(request,'Proveedor Eliminado')
#        return redirect('')

