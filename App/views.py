from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from django.http.response import JsonResponse
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from App.models import Proveedor, Empleado, Compra,Producto,Venta, Reporte, HistorialInventario, SeleccionProducto
from .forms import ProveedorForm, EmpleadoForm, CompraForm,ProductoForm, SeleccionProductoForm



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

def actualizar_empleado(request, empleado_id):
    empleado=get_object_or_404(Empleado, id=empleado_id)
    form=EmpleadoForm(instance=empleado)
    if request.method == 'POST':
        form=EmpleadoForm(request.POST,instance=empleado)
        if form.is_valid():
            form.save()
        return redirect('empleados_ver')
    data={'form':form,'titulo':'Empleado actualizado'}
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
    total = 0

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
    for item in productos_carrito:
        item['precio_final'] = item['precio_unitario'] * item['cantidad'] * (1 - item['descuento'] / 100)
        total += item['precio_final']

    

    return render(request, 'carrito.html', {'productos_carrito': productos_carrito, 'total': total})

def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
    
    request.session['carrito'] = carrito
    return redirect('carrito')
"""
View ventas 
"""
def generar_venta(request):
    carrito = request.session.get('carrito', {})
    total_venta = 0  # Total de la venta
    detalles_venta = []

    # Recorremos el carrito para procesar cada producto
    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.get(id=producto_id)
        precio_unitario_con_descuento = producto.precio_con_descuento()  # Precio con descuento

        # Verificamos si hay suficiente stock
        if producto.cantidad >= cantidad:
            # Crear la venta para cada producto
            venta = Venta.objects.create(
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario_con_descuento,
                detalles=f"Venta de {cantidad} unidades de {producto.nombre}"
            )

            # Actualizar el stock del producto
            producto.cantidad -= cantidad
            producto.save()

            # Calculamos el total de la venta
            total_venta += venta.total()  # Llama al método total() que calcula cantidad * precio_unitario
            detalles_venta.append({
                'producto': producto.nombre,
                'cantidad': cantidad,
                'precio_unitario': precio_unitario_con_descuento,
                'total': venta.total(),
                'descuento': producto.descuento,  # Incluimos el descuento
                'precio_final': precio_unitario_con_descuento * (1 - producto.descuento / 100),  # Precio final con descuento
            })
        else:
            # Si no hay suficiente stock, puedes mostrar un mensaje o redirigir
            return render(request, 'carrito.html', {'mensaje': 'No hay suficiente stock para algunos productos.'})

    # Limpiar el carrito después de la venta
    request.session['carrito'] = {}

    # Crear un PDF con los detalles de la venta
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="boleto_venta.pdf"'

    # Crear el objeto canvas de ReportLab para el PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    # Agregar detalles de la venta al PDF
    p.drawString(100, 750, "Boleto de Venta")
    p.drawString(100, 730, f"Fecha: {venta.fecha}")
    
    

    # Dibujar encabezados de la tabla
    p.rect(50, 670, 500, 20)  # Caja para la cabecera de la tabla
    p.drawString(100, 675, "Producto")
    p.drawString(250, 675, "Cantidad")
    p.drawString(350, 675, "Precio Unitario")
    p.drawString(450, 675, "Total")

    # Listar los productos comprados
    y_position = 650  # Posición inicial para los productos
    for detalle in detalles_venta:
        p.drawString(100, y_position, f"{detalle['producto']}")
        p.drawString(250, y_position, f"{detalle['cantidad']}")
        p.drawString(350, y_position, f"${detalle['precio_unitario']:.2f}")
        p.drawString(450, y_position, f"${detalle['total']:.2f}")

        # Mostrar descuento si hay
        if detalle['descuento'] > 0:
            p.drawString(100, y_position - 20, f"Descuento: {detalle['descuento']}%")
            p.drawString(250, y_position - 20, f"Precio Final con Descuento: ${detalle['precio_final']:.2f}")
        
        # Dibujar una línea después de cada producto
        p.line(50, y_position - 10, 550, y_position - 10)

        y_position -= 40  # Espacio para el siguiente producto

    # Agregar el total de la venta al final
    p.drawString(100, y_position - 20, f"Total de la Venta: ${total_venta:.2f}")

    # Cerrar el PDF
    p.showPage()
    p.save()

    # Redirigir al catálogo después de generar el PDF
    return response

"""
View Inventario 
"""


def deshabilitados_ver (request):
    return render(request, 'productosDeshabilitados.html')

def listaDeshabilitados (request):

    productos = Producto.objects.filter(habilitado= False)  # Filtra solo los productos Desactivados
    productos_data = [
        {
            'id': producto.id,
            'nombre': producto.nombre,
            'cantidad': producto.cantidad,
            'precio': producto.precio,
        }
        for producto in productos
    ]
    return JsonResponse({'productos': productos_data})

def inventario_ver(request):
    return render(request, 'inventario_verP.html')

def lista_productos(request):
    productos = Producto.objects.filter(habilitado= True)  # Filtra solo los productos activos
    productos_data = [
        {
            'id': producto.id,
            'nombre': producto.nombre,
            'cantidad': producto.cantidad,
            'precio': producto.precio,
        }
        for producto in productos
    ]
    return JsonResponse({'productos': productos_data})

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

def habilitar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.habilitado = True
    producto.save()
    messages.success(request, f'Producto {producto.nombre} habilitado.')
    return redirect('ver_deshabilitados') 

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

def productos_mayor_variacion(request):
    productos_variacion = (
        HistorialInventario.objects.values('producto__id', 'producto__nombre')
        .annotate(
            total_variacion=Coalesce(Sum('cantidad'), Value(0))
        )
        .order_by('-total_variacion')[:10] 
    )
    return render(request, '#', {'productos_variacion': productos_variacion})

def seleccionar_producto(request):
    if request.method == 'POST':
        form = SeleccionProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_seleccion')  # Cambia por la ruta de tu lista de selección
    else:
        form = SeleccionProductoForm()

    return render(request, 'seleccionar_producto.html', {'form': form})

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
    return redirect('proveedores_ver')

def actualizar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor Actualizado')
            return redirect('proveedores_ver')  # Redirige a la lista de proveedores después de actualizar
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

