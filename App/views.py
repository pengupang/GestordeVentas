from django.shortcuts import render

# Create your views here.
def login (request):
    return render(request,'login.html')

def inicio (request):
    return render(request,'inicio.html')

def empleados (request):
    return render (request,'empleados.html')

def agregar_Empleado (request):
    return render(request,'empleados_agregar.html')

def catalogo (request):
    return render(request,'catalogo.html')