"""
URL configuration for GestordeVentas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', views.inicio),
    path('',views.login),
    path('empleados_ver/',views.empleados),
    path('empleados_agregar/',views.agregar_empleado),
    path('catalogo/',views.catalogo),
    path('inventario_compra/',views.inventario_compra),
    path('inventario_ver/',views.inventario_ver),
    path('proveedor_ver/',views.proveedores_ver),
    path('proveedor_ingresar/',views.proveedores_ingresar)

]
