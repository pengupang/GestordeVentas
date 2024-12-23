from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F, Value, Count, Q
from django.db.models.functions import Coalesce
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils import timezone
from datetime import datetime
from plotly.offline import plot
import plotly.graph_objs as go  
import json
from functools import wraps

from App.models import Proveedor, Empleado, Compra,Producto,Venta, Reporte, HistorialInventario, SeleccionProducto
from .forms import ProveedorForm, EmpleadoForm, CompraForm,ProductoForm, SeleccionProductoForm



# Create your views here.
def login(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')  # Recibimos el nombre del formulario
        contrasena = request.POST.get('password')

        try:
            empleado = Empleado.objects.get(nombre=nombre)  # Busca el empleado por nombre
        except Empleado.DoesNotExist:
            messages.error(request, 'El usuario no existe.')
            return redirect('login')

        # Comparar las contraseñas directamente (sin encriptación)
        if contrasena == empleado.contrasena:  # Verifica la contraseña directamente
            if not empleado.habilitado:
                messages.error(request, 'Tu cuenta está deshabilitada.')
                return redirect('login')

            # Autenticación exitosa, guardar datos en sesión
            request.session['empleado_id'] = empleado.id
            request.session['empleado_tipo'] = empleado.tipo
            messages.success(request, f'Bienvenido {empleado.nombre}')
            return redirect('inicio')  # Redirige a la vista principal
        else:
            messages.error(request, 'Contraseña incorrecta.')
    return render(request, 'login.html')






def verificar_permiso(roles_permitidos):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            empleado_tipo = request.session.get('empleado_tipo')
            
            if 'empleado_id' not in request.session:
                return redirect('login')  # Redirige al login si no está autenticado
            
            if empleado_tipo == 'Manager':  # Managers tienen acceso total
                return func(request, *args, **kwargs)
            
            if empleado_tipo not in roles_permitidos:  # Restringe el acceso según el rol
                messages.error(request, 'No tienes acceso a esta sección.')
                return redirect('inicio')  # Redirige a la vista de empleados o cualquier vista accesible

            return func(request, *args, **kwargs)
        return wrapper
    return decorator

""" 
Dashboard
"""
def inicio(request):
    # Obtener ventas por mes
    ventas_por_mes = Venta.objects.values('fecha__month').annotate(
        total_ventas=Sum('cantidad'),
        total_monto=Sum('precio_unitario')
    ).order_by('fecha__month')

    # Crear los datos para los gráficos
    meses = [str(x['fecha__month']) for x in ventas_por_mes]
    cantidad_ventas = [x['total_ventas'] for x in ventas_por_mes]
    monto_recaudado = [x['total_monto'] for x in ventas_por_mes]

    # Configuración para desactivar las opciones interactivas
    config = {
        'displayModeBar': False,
        'scrollZoom': False,
        'showTips': False,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['toImage', 'zoomIn2d', 'zoomOut2d']
    }

    # Gráfico de dinero recaudado por mes (Barras)
    trace1 = go.Bar(
        x=meses,
        y=monto_recaudado,
        marker=dict(color='rgb(96, 172, 208)')
    )

    # Gráfico de cantidad de ventas por mes (Líneas o Puntos)
    trace2 = go.Scatter(
        x=meses,
        y=cantidad_ventas,
        mode='lines+markers',
        name='Cantidad de ventas',
        marker=dict(color='rgb(96, 172, 208)', size=10),
        line=dict(width=2)
    )

    # Layout para el gráfico de barras
    layout1 = go.Layout(
        xaxis={'title': 'Mes'},
        yaxis={'title': 'Dinero (CLP)'},
        width=400,   # Ancho del gráfico
        height=230, # Alto del gráfico
        margin=dict(l=100, r=0, t=0, b=0),
    )
    fig1 = go.Figure(data=[trace1], layout=layout1)
    graph_html1 = plot(fig1, output_type='div', config=config)

    # Layout para el gráfico de líneas
    layout2 = go.Layout(
        xaxis={'title': 'Mes'},
        yaxis={'title': 'Cantidad de Ventas'},
        width=400,   # Ancho del gráfico
        height=230, # Alto del gráfico
        margin=dict(l=100, r=0, t=0, b=0),
    )
    fig2 = go.Figure(data=[trace2], layout=layout2)
    graph_html2 = plot(fig2, output_type='div', config=config)

    # Obtener la fecha de hoy y filtrar ventas de hoy
    today = timezone.now().date()
    start_of_day = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_of_day = timezone.make_aware(datetime.combine(today, datetime.max.time()))

    # Filtrar las ventas realizadas hoy
    venta_diaria = Venta.objects.filter(
        fecha__gte=start_of_day,
        fecha__lte=end_of_day
    ).aggregate(total_ventas=Sum('cantidad'))

    # Obtener los productos vendidos hoy
    productos_vendidos = Venta.objects.filter(
        fecha__gte=start_of_day,
        fecha__lte=end_of_day
    ).values('producto__nombre', 'producto__imagen').annotate(total_vendido=Sum('cantidad'))

    # Preparar los datos para el gráfico de dona
    productos = [x['producto__nombre'] for x in productos_vendidos]
    cantidades = [x['total_vendido'] for x in productos_vendidos]

    # Crear el gráfico de dona
    trace3 = go.Pie(
        labels=productos,
        values=cantidades,
        hole=0.4,
        marker=dict(colors=['rgb(96, 172, 208)', 'rgb(129, 194, 216)', 'rgb(162, 217, 239)']),
    )
    layout3 = go.Layout(
        width=300,   # Ancho del gráfico
        height=230, # Alto del gráfico
        margin=dict(l=20, r=0, t=0, b=0),  # Sin márgenes
        showlegend=False 
    )
    fig3 = go.Figure(data=[trace3], layout=layout3)
    graph_html3 = plot(fig3, output_type='div', config=config)
    
    
    producto_mas_vendido = productos_vendidos.order_by('-total_vendido').first()

    producto_mas_vendido_imagen = None
    if producto_mas_vendido:
        producto_mas_vendido_nombre = producto_mas_vendido['producto__nombre']
        producto_mas_vendido_imagen = producto_mas_vendido.get('producto__imagen', None)
        print(f"Imagen dinámica: {producto_mas_vendido_imagen}")
    else:
        producto_mas_vendido_nombre = 'No hay ventas'
        producto_mas_vendido_imagen = None
    # Obtener el producto más vendido
    producto_mas_vendido = max(productos_vendidos, key=lambda x: x['total_vendido'], default=None)
   

    # Pasar los datos al template
    return render(request, 'inicio.html', {
        'graph_html1': graph_html1,
        'graph_html2': graph_html2,
        'ventasD': venta_diaria['total_ventas'] or 0,
        'graph_html3': graph_html3,
        'producto_mas_vendido': producto_mas_vendido_nombre,
        'producto_mas_vendido_imagen': producto_mas_vendido_imagen,
    })

"""
View Empleados 
"""

@verificar_permiso(['Manager'])
def empleados (request):
    empleado = Empleado.objects.filter(habilitado=True)
    return render(request, 'empleados_ver.html', {'empleado': empleado})

@verificar_permiso(['Manager'])
def agregar_empleado(request):
    form = EmpleadoForm()
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado Ingresado') #Mensaje de empleado ingresado
            return redirect('../empleados/') 
        else:
            messages.error(request, 'Error empleado no ingresado') # Mensaje de error
    data = {'form': form }
    return render(request,'empleados_agregar.html',data)

@verificar_permiso(['Manager'])
def actualizar_empleado(request, empleado_id):
    empleado=get_object_or_404(Empleado, id=empleado_id)
    form=EmpleadoForm(instance=empleado)
    if request.method == 'POST':
        form=EmpleadoForm(request.POST,instance=empleado)
        if form.is_valid():
            form.save()
        return redirect('empleados')
    data={'form':form,'titulo':'Empleado Actualizar'}
    return render(request,'empleados_agregar.html',data)

@verificar_permiso(['Manager'])
def empleados_ver(request):
    query = request.GET.get('q', '')

    empleados = Empleado.objects.filter(
        Q(nombre__icontains=query) | 
        Q(apellido__icontains=query) | 
        Q(email__icontains=query) | 
        Q(tipo__icontains=query)
    )

    paginator = Paginator(empleados, 10) 
    page_number = request.GET.get('page', 1)
    empleados_paginados = paginator.get_page(page_number)
    return render(request, 'empleados_ver.html', {
        'empleado': empleados_paginados,  
        'query': query, 
    })


@verificar_permiso(['Manager'])
def deshabilitar_empleado(request, empleado_id):
    empleados = get_object_or_404(Empleado, id=empleado_id)
    empleados.habilitado = False  
    empleados.save()
    messages.success(request, f'Empleado {empleados.nombre} deshabilitado.')
    return redirect('empleados')
    

"""
View Catalago 
"""
@verificar_permiso(['Manager','Vendedor'])
def catalogo_view(request):
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query, habilitado=True)
    else:
        productos = Producto.objects.filter(habilitado=True)
    
    return render(request, 'catalogo.html', {'productos': productos})

@verificar_permiso(['Manager','Vendedor'])
def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    # Asegúrate de usar cadenas como claves si la sesión las guarda así
    producto_id = str(producto_id)
    carrito[producto_id] = carrito.get(producto_id, 0) + 1
    request.session['carrito'] = carrito
    return redirect('carrito')  # Redirige al carrito después de agregar

@verificar_permiso(['Manager','Vendedor'])
def disminuir_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id = str(producto_id)
    if producto_id in carrito:
        if carrito[producto_id] > 1:
            carrito[producto_id] -= 1  # Disminuye la cantidad
        else:
            del carrito[producto_id]  # Elimina el producto si la cantidad es 0
    request.session['carrito'] = carrito
    return redirect('carrito')  # Redirige al carrito después de disminuir

@verificar_permiso(['Manager','Vendedor'])
def actualizar_carrito(request, id_producto, accion):
    carrito = request.session.get('carrito', {})
    id_producto = str(id_producto)  # Asegúrate de manejar las claves como cadenas
    confirmar_eliminacion = False

    try:
        if accion == 'aumentar':
            carrito[id_producto] = carrito.get(id_producto, 0) + 1
        elif accion == 'disminuir':
            if carrito.get(id_producto, 0) == 1:
                confirmar_eliminacion = True  # Marca para confirmación
            elif carrito.get(id_producto, 0) > 1:
                carrito[id_producto] -= 1
            else:
                del carrito[id_producto]  # Elimina si la cantidad es 0

        request.session['carrito'] = carrito  # Guarda el carrito actualizado
        return JsonResponse({'success': True, 'confirmar_eliminacion': confirmar_eliminacion})
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'success': False}, status=400)

@verificar_permiso(['Manager', 'Bodeguero','Vendedor'])
def ver_carrito(request):
    carrito = request.session.get('carrito', {})  # Suponiendo que el carrito se guarda en la sesión
    productos_carrito = []
    total = 0

    # Recolecta productos en el carrito
    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.get(id=producto_id)
        precio_final = producto.precio_con_descuento()
        productos_carrito.append({
            'id' : producto_id,
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

@verificar_permiso(['Manager','Vendedor'])
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
    
    request.session['carrito'] = carrito
    return redirect('carrito')
"""
View ventas 
"""
@verificar_permiso(['Manager','Vendedor'])
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

            # Actualizamos el stock del producto
            producto.cantidad -= cantidad
            producto.save()

            # Verificamos si la cantidad llegó a 0 y deshabilitamos el producto
            if producto.cantidad == 0:
                producto.habilitado = False
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
    p.drawString(100, 750, "Comprobante de Venta")
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
            p.drawString(100, y_position - 30, f"Descuento: {detalle['descuento']}%")
            p.drawString(250, y_position - 30, f"Precio Final con Descuento: ${detalle['precio_final']:.2f}")
        
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
    productos = Producto.objects.filter(habilitado=True)  # Filtra solo los productos habilitados
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


@verificar_permiso(['Manager'])
def actualizar_inventario(request, id):
    producto = get_object_or_404(Producto, id=id)
    form = ProductoForm(instance=producto)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.actualizado_por = request.user.username  
            producto.razon_actualizacion = form.cleaned_data['razon_actualizacion']  
            producto.save()

            # Verificar si llegó a 0
            if producto.cantidad == 0:
                producto.habilitado = False
                producto.save()

            messages.success(request, 'Inventario actualizado correctamente.')
            return redirect('inventario_ver')
        else:
            messages.error(request, 'Error al actualizar el inventario.')

    return render(request, 'producto_actualizar.html', {'form': form, 'producto': producto})


@verificar_permiso(['Manager'])
def reducir_cantidad_producto(request, producto_id, cantidad):
    """
    Reduce la cantidad de un producto en el inventario.
    """
    producto = get_object_or_404(Producto, id=producto_id)

    # Verificar si la cantidad a reducir no excede el stock
    if cantidad > producto.cantidad:
        messages.error(request, f"La cantidad a reducir ({cantidad}) excede el stock disponible ({producto.cantidad}).")
        return JsonResponse({'error': 'Cantidad excede el stock disponible'}, status=400)

    # Reducir la cantidad del producto
    producto.cantidad -= cantidad
    producto.save()

    # Verificar si la cantidad está por debajo del mínimo
    if producto.cantidad <= producto.cantidad_minima:
        messages.warning(request, f"¡Advertencia! El producto '{producto.nombre}' tiene solo {producto.cantidad} unidades disponibles, ¡está por debajo del mínimo de {producto.cantidad_minima} unidades!")

    messages.success(request, f"Se redujeron {cantidad} unidades del producto '{producto.nombre}'.")
    return JsonResponse({'message': 'Cantidad reducida exitosamente', 'nueva_cantidad': producto.cantidad})

#def productos_bajo_stock(request):
#    productos_bajo_stock = Producto.objects.filter(cantidad__lte=models.f('cantidad_minima'))
#    return render(request, 'productos_bajo_stock.html', {'productos_bajo_stock': productos_bajo_stock})

@verificar_permiso(['Manager', 'Bodeguero','Vendedor'])
def historial_inventario(request):
    # Obtener todo el historial (entradas y salidas)
    historial = HistorialInventario.objects.all().order_by('-fecha')  # Ordenar por fecha descendente
    return render(request, 'historial_inventario.html', {'historial': historial})

@verificar_permiso(['Manager', 'Bodeguero'])
def agregar_producto(request):
    form = ProductoForm()
    if request.method == 'POST':
        form = ProductoForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto Ingresado') # Mensaje de producto ingresado
            return redirect('inventario_ver') 
        else:
            messages.error(request, 'Error producto no ingresado') # Mensaje de error
    data = {'form': form }
    return render(request,'producto_agregar.html',data)

@verificar_permiso(['Manager'])
def deshabilitar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.habilitado = False
    producto.save()
    messages.success(request, f'Producto {producto.nombre} deshabilitado.')
    return redirect('inventario_ver') 

@verificar_permiso(['Manager'])
def habilitar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.habilitado = True
    producto.save()
    messages.success(request, f'Producto {producto.nombre} habilitado.')
    return redirect('ver_deshabilitados') 

@verificar_permiso(['Manager'])
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

@verificar_permiso(['Manager', 'Bodeguero','Vendedor'])
def seleccionar_producto(request):
    if request.method == 'POST':
        form = SeleccionProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_seleccion')  # Cambia por la ruta de tu lista de selección
    else:
        form = SeleccionProductoForm()

    return render(request, 'seleccionar_producto.html', {'form': form})

@verificar_permiso(['Manager'])
def editar_compra(request, id):
    compra = get_object_or_404(Compra, id=id)
    if request.method == 'POST':
        form = CompraForm(request.POST, instance=compra)
        if form.is_valid():
            form.save()
            return redirect('compras_ver') 
    else:
        form = CompraForm(instance=compra)
    
    return render(request, 'inventario_compras.html', {
        'form': form,
        'compra': compra,
        'titulo': 'Editar Compra' 
    })

"""
View Proveedores 
"""

@verificar_permiso(['Manager'])
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

@verificar_permiso(['Manager'])
def proveedores_ver(request):
    proveedor = Proveedor.objects.all()
    data = {'proveedor':proveedor}
    return render(request,'proveedores_ver.html',data)

@verificar_permiso(['Manager'])
def deshabilitar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    proveedor.habilitado = False  
    proveedor.save()
    messages.success(request, f'Proveedor {proveedor.Nombre} deshabilitado.')
    return redirect('proveedores_ver')

@verificar_permiso(['Manager'])
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
@verificar_permiso(['Manager', 'Bodeguero'])
def compra_agregar(request):
    last_compra = Compra.objects.order_by('id').last()
    next_id = last_compra.id + 1 if last_compra else 1

    if request.method == "POST":
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)  

            compra.orden = next_id
            compra.save()

            
            producto = compra.producto  
            cantidad_comprada = compra.cantidad

           
            producto.cantidad += cantidad_comprada
            producto.save()

            messages.success(request, f"Compra registrada correctamente. Se han agregado {cantidad_comprada} unidades de '{producto.nombre}' al inventario.")
            return redirect('inventario_ver') 

    else:
        form = CompraForm()

    productos = Producto.objects.all()  # Obtener todos los productos para mostrarlos en el formulario

    context = {
        'form': form,
        'titulo': 'Agregar Compra',
        'productos': productos,
        'next_id': next_id,
    }

    return render(request, 'inventario_compras.html', context)
@verificar_permiso(['Manager', 'Bodeguero'])
def compras_Ver (request):
    compras = Compra.objects.filter(habilitado=True)
    data = {'compra':compras}
    return render(request,'compras_ver.html',data)

@verificar_permiso(['Manager'])
def compra_deshabilitar(request,compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    compra.habilitado = False
    compra.save()
    messages.success(request, f'Producto {compra.producto} deshabilitado.')
    return redirect('compras_ver') 

@verificar_permiso(['Manager'])
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


@verificar_permiso(['Manager', 'Bodeguero'])
def generar_reporte(request):
    compras = []
    ventas = []
    grafico_data = None  # Datos para el gráfico

    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_final = request.POST.get('fecha_final')
        tipo_reporte = request.POST.get('tipo_reporte')

        # Filtrar las compras y ventas según las fechas
        if tipo_reporte in ['compra', 'ambos']:
            compras = Compra.objects.filter(fecha__range=[fecha_inicio, fecha_final])
        if tipo_reporte in ['venta', 'ambos']:
            ventas = Venta.objects.filter(fecha__range=[fecha_inicio, fecha_final])

        # Guardar los resultados en la sesión
        request.session['compras'] = [compra.id for compra in compras]
        request.session['ventas'] = [venta.id for venta in ventas]

        # Preparar datos para el gráfico
        if compras or ventas:
            fechas_comunes = set()
            compras_data = {}
            ventas_data = {}

            # Procesar compras
            for compra in compras:
                fecha_str = compra.fecha.strftime('%Y-%m-%d')
                fechas_comunes.add(fecha_str)
                compras_data[fecha_str] = compras_data.get(fecha_str, 0) + float(compra.precio)

            # Procesar ventas
            for venta in ventas:
                fecha_str = venta.fecha.strftime('%Y-%m-%d')
                fechas_comunes.add(fecha_str)
                ventas_data[fecha_str] = ventas_data.get(fecha_str, 0) + float(venta.precio_unitario) * venta.cantidad

            # Ordenar fechas y preparar valores
            fechas_ordenadas = sorted(fechas_comunes)
            compras_valores = [compras_data.get(fecha, 0) for fecha in fechas_ordenadas]
            ventas_valores = [ventas_data.get(fecha, 0) for fecha in fechas_ordenadas]

            # Preparar los datasets del gráfico
            grafico_data = {
                'labels': fechas_ordenadas,
                'datasets': [
                    {
                        'label': 'Compras',
                        'data': compras_valores,
                        'borderColor': 'rgba(75, 192, 192, 1)',
                        'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                        'borderWidth': 2,
                        'fill': False,
                    },
                    {
                        'label': 'Ventas',
                        'data': ventas_valores,
                        'borderColor': 'rgba(255, 99, 132, 1)',
                        'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                        'borderWidth': 2,
                        'fill': False,
                    }
                ]
            }

    else:
        # Recuperar los resultados de la sesión
        if 'compras' in request.session or 'ventas' in request.session:
            compras_ids = request.session.get('compras', [])
            ventas_ids = request.session.get('ventas', [])
            compras = Compra.objects.filter(id__in=compras_ids)
            ventas = Venta.objects.filter(id__in=ventas_ids)

            # Preparar datos para el gráfico (sesión)
            if compras or ventas:
                fechas_comunes = set()
                compras_data = {}
                ventas_data = {}

                # Procesar compras
                for compra in compras:
                    fecha_str = compra.fecha.strftime('%Y-%m-%d')
                    fechas_comunes.add(fecha_str)
                    compras_data[fecha_str] = compras_data.get(fecha_str, 0) + float(compra.precio)

                # Procesar ventas
                for venta in ventas:
                    fecha_str = venta.fecha.strftime('%Y-%m-%d')
                    fechas_comunes.add(fecha_str)
                    ventas_data[fecha_str] = ventas_data.get(fecha_str, 0) + float(venta.precio_unitario) * venta.cantidad

                # Ordenar fechas y preparar valores
                fechas_ordenadas = sorted(fechas_comunes)
                compras_valores = [compras_data.get(fecha, 0) for fecha in fechas_ordenadas]
                ventas_valores = [ventas_data.get(fecha, 0) for fecha in fechas_ordenadas]

                # Preparar los datasets del gráfico
                grafico_data = {
                    'labels': fechas_ordenadas,
                    'datasets': [
                        {
                            'label': 'Compras',
                            'data': compras_valores,
                            'borderColor': 'rgba(75, 192, 192, 1)',
                            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                            'borderWidth': 2,
                            'fill': False,
                        },
                        {
                            'label': 'Ventas',
                            'data': ventas_valores,
                            'borderColor': 'rgba(255, 99, 132, 1)',
                            'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                            'borderWidth': 2,
                            'fill': False,
                        }
                    ]
                }

    return render(request, 'reportes.html', {
        'compras': compras,
        'ventas': ventas,
        'grafico_data': json.dumps(grafico_data) if grafico_data else None
    })












#def eliminar_proveedor(request, id):
#    proveedor = get_object_or_404(Proveedor, id = id)
#    if request.method == 'POST':
#        proveedor.delete()
#        messages.success(request,'Proveedor Eliminado')
#        return redirect('')

