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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', views.inicio),
    path('',views.login),
    path('empleados_ver/',views.empleados),
    path('empleados_agregar/',views.agregar_empleado),

    path('catalogo/',views.catalogo_view,name= 'catalogo'),
     path('carrito/', views.ver_carrito, name='carrito'),
     path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('disminuir/<int:producto_id>/', views.disminuir_del_carrito, name='disminuir_del_carrito'),
    path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

    path('compras_ver/', views.compras_Ver, name='compras_ver'),
    path('compras_ver/deshabilitar/<int:compra_id>',views.compra_deshabilitar, name='deshabilitar_compra'),
    path('inventario_compras/<int:id>', views.compra_editar, name='inventario_editar'),
    path('inventario_compras/', views.compra_agregar, name='inventario_compras'),
    path('inventario_ver/', views.inventario_ver, name='inventario_ver'),
    path('inventario/deshabilitar/<int:producto_id>/', views.deshabilitar_producto, name='deshabilitar_producto'),
    path('producto_agregar/',views.agregar_producto),
    path ('listaProductos/',views.lista_productos,name='lista_productos'),
    path ('deshabilitados/',views.listaDeshabilitados,name='listaDeshabilitados'),
    path('deshabilitados_ver',views.deshabilitados_ver,name='ver_deshabilitadosP'),
    path('inventario/habilitar/<int:producto_id>/',views.habilitar_producto,name='habilitar'),
    path('proveedor_ver/',views.proveedores_ver),
    path('proveedor_ingresar/',views.proveedores_ingresar),
    path('proveedor/deshabilitar/<int:proveedor_id>/', views.deshabilitar_proveedor, name='deshabilitar_proveedor'),
    path('proveedor/actualizar/<int:proveedor_id>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    path('generar-reporte/', views.generar_reporte, name='generar_reporte'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

