from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from App.models import Proveedor, Empleado, Compra,Producto
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
    return render (request,'empleados_ver.html')

def agregar_empleado(request):
    form = EmpleadoForm()
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado Ingresado')
            return redirect('empleados_agregar/') 
        else:
            messages.error(request, 'Error empleado no ingresado')
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
def catalogo (request):
    return render(request,'catalogo.html')

"""
View Inventario 
"""

def inventario_ver(request):
    productos = Producto.objects.filter(habilitado=True)
    return render(request, 'inventario_ver.html', {'productos': productos})

def actualizar_inventario(request,id):
    productos=Producto.objects.get(id=id)
    form=ProductoForm(instance= productos)
    if request.method=="POST":
        form=ProductoForm(request.POST,instance=productos)
        if form.is_valid():
            form.save()
        return inventario_ver(request)
    data={'form':form,'titulo':'Actualizar Inventario'}
    return render(request,'inventario_ver.html',data)

def deshabilitar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.habilitado = False
    producto.save()
    messages.success(request, f'Producto {producto.producto} deshabilitado.')
    return redirect('inventario_ver') 

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
            return redirect('proveedor_ver/')
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
            return redirect('lista_proveedores')  # Redirige a la lista de proveedores después de actualizar
    else:
        form = ProveedorForm(instance=proveedor)
    
    return render(request, 'actualizar_proveedor.html', {'form': form, 'proveedor': proveedor})

"""
View Compras 
"""
def compra_Agregar(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('compras_ver')  
    else:
        form = CompraForm()
    
    return render(request, 'inventario_compras.html', {'form': form, 'titulo':'ingresar Compra'})

def compras_Ver (request):
    compra = Compra.objects.all()
    data = {'compra':compra}
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

#def eliminar_proveedor(request, id):
#    proveedor = get_object_or_404(Proveedor, id = id)
#    if request.method == 'POST':
#        proveedor.delete()
#        messages.success(request,'Proveedor Eliminado')
#        return redirect('')

