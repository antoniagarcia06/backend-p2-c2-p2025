from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('producto/nuevo/', views.nuevo_producto, name='nuevo_producto'),
    path('producto/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),

    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('cliente/nuevo/', views.nuevo_cliente, name='nuevo_cliente'),

    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('venta/nueva/', views.nueva_venta, name='nueva_venta'),
    path('venta/<int:id>/', views.detalle_venta, name='detalle_venta'),
]
