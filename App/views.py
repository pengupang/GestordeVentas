from django.shortcuts import render
from App.models import Proveedor
from .forms import ProveedorForm



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

def agregar_Empleado (request):
    return render(request,'empleados_agregar.html')

"""
View Catalago 
"""
def catalogo (request):
    return render(request,'catalogo.html')

"""
View Inventario 
"""
def inventario_compra (request):
    return render(request,'inventario_compras.html')
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
    data = {'form': form }
    return render(request,'proveedores_ingresar.html',data)

def proveedores_ver(request):
    proveedor = Proveedor.objects.all()
    data = {'proveedor':proveedor}
    return render(request,'proveedores_ver.html',data)