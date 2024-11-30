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
    # Admin
    path('admin/', admin.site.urls),

    # Autenticación
    path('', views.login, name='login'),
    path('inicio/', views.inicio, name='inicio'),

    # Empleados
    path('empleados/', views.empleados, name='empleados_ver'),
    path('empleados/agregar/', views.agregar_empleado, name='empleados_agregar'),
    path('empleados/actualizar/<int:empleado_id>/', views.actualizar_empleado, name='empleados_actualizar'),
    path('empleados/deshabilitar/<int:empleado_id>/', views.deshabilitar_empleado, name='empleados_deshabilitar'),
    path('empleados_agregar/', views.agregar_empleado, name='empleados_agregar'),

    # Catálogo y carrito
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('carrito/', views.ver_carrito, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='carrito_agregar'),
    path('carrito/disminuir/<int:producto_id>/', views.disminuir_del_carrito, name='carrito_disminuir'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='carrito_eliminar'),

    # Inventario
    path('inventario/', views.inventario_ver, name='inventario_ver'),
    path('inventario/agregar/', views.agregar_producto, name='producto_agregar'),
    path('inventario/actualizar/<int:id>/', views.actualizar_inventario, name='inventario_actualizar'),
    path('inventario/deshabilitar/<int:producto_id>/', views.deshabilitar_producto, name='producto_deshabilitar'),
    path('inventario/habilitar/<int:producto_id>/', views.habilitar_producto, name='producto_habilitar'),
    path('inventario/deshabilitados/', views.deshabilitados_ver, name='ver_deshabilitados'),
    path('inventario/lista/', views.lista_productos, name='lista_productos'),
    path('inventario/deshabilitados/lista/', views.listaDeshabilitados, name='lista_deshabilitados'),
    path('inventario/historial/', views.historial_inventario, name='historial_inventario'),
    path('inventario/variacion/', views.productos_mayor_variacion, name='productos_mayor_variacion'),

    # Proveedores
    path('proveedores/', views.proveedores_ver, name='proveedores_ver'),
    path('proveedores/agregar/', views.proveedores_ingresar, name='proveedores_agregar'),
    path('proveedores/actualizar/<int:proveedor_id>/', views.actualizar_proveedor, name='proveedores_actualizar'),
    path('proveedores/deshabilitar/<int:proveedor_id>/', views.deshabilitar_proveedor, name='proveedores_deshabilitar'),
    path('proveedor_ingresar/', views.proveedores_ingresar, name='proveedores_ingresar'), 
    path('proveedor_ver/', views.proveedores_ver, name='proveedores_ver'),

    # Compras
    path('compras/', views.compras_Ver, name='compras_ver'),
    path('compras/agregar/', views.compra_agregar, name='compras_agregar'),
    path('compras/actualizar/<int:id>/', views.compra_editar, name='compras_actualizar'),
    path('compras/deshabilitar/<int:compra_id>/', views.compra_deshabilitar, name='compras_deshabilitar'),
    path('compras/inventario_ver/', views.inventario_ver, name='compras_inventario_ver'),
    path('compras/editar/<int:id>/', views.editar_compra, name='compras_editar'),

    # Reportes
    path('reportes/', views.generar_reporte, name='generar_reporte'),

    #Ventas
    path('venta/',views.generar_venta,name='venta')

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

