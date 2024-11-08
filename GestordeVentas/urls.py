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
    path('compras_ver/', views.compras_Ver, name='compras_ver'),
    path('compras_ver/deshabilitar',views.compra_deshabilitar),
    path('inventario_compras/<int:id>', views.compra_editar, name='inventario_compras'),
    path('inventario_compras/', views.compra_Agregar, name='inventario_compras'),
    path('inventario_ver/', views.inventario_ver, name='inventario_ver'),
    path('inventario/deshabilitar/', views.deshabilitar_producto, name='deshabilitar_producto'),
    path('proveedor_ver/',views.proveedores_ver),
    path('proveedor_ingresar/',views.proveedores_ingresar),
    path('proveedor/deshabilitar/<int:proveedor_id>/', views.deshabilitar_proveedor, name='deshabilitar_proveedor'),
    path('proveedor/actualizar/<int:proveedor_id>/', views.actualizar_proveedor, name='actualizar_proveedor')

]
