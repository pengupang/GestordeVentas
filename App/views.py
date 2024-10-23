from django.shortcuts import render

# Create your views here.
def login (request):
    return render(request,'login.html')

def inicio (request):
    return render(request,'inicio.html')

def empleados (request):
    return render (request,'empleados_ver.html')

def agregar_Empleado (request):
    return render(request,'empleados_agregar.html')

def catalogo (request):
    return render(request,'catalogo.html')

def inventario_compra (request):
    return render(request,'inventario_compras.html')
def inventario_ver (request):
    return render(request,'inventario_ver.html')

def proveedores_ingresar(request):
    return render(request,'proveedores_ingresar.html')
def proveedores_ver(request):
    return render(request,'proveedores_ver.html')