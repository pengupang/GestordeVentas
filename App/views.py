from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from App.models import Proveedor, Empleado
from .forms import ProveedorForm, EmpleadoForm, CompraForm



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
    

"""
View Catalago 
"""
def catalogo (request):
    return render(request,'catalogo.html')

"""
View Inventario 
"""
def inventario_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('inventario_ver.html')  
    else:
        form = CompraForm()
    
    return render(request, 'inventario_compras.html', {'form': form})
def inventario_ver (request):
    return render(request,'inventario_ver.html')

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

#def eliminar_proveedor(request, id):
#    proveedor = get_object_or_404(Proveedor, id = id)
#    if request.method == 'POST':
#        proveedor.delete()
#        messages.success(request,'Proveedor Eliminado')
#        return redirect('')



