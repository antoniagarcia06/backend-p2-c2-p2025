from django.urls import path
from . import views
urlpatterns = [
    path("", views.lista_productos, name="lista_productos"),
    path ("productos/", views.lista_productos, name="lista_productos"),
    path("productos/<int:id>/", views.nuevo_producto, name="nuevo_producto"),
    path("producto/editar/<int:id>/", views.editar_producto, name="editar_producto"),
    path("producto/eliminar/<int:id>/", views.eliminar_producto, name="eliminar_producto"),

    path("venta/nueva/", views.registrar_venta, name="registrar_venta"),
    path("venta/<int:id>/", views.detalle_venta, name="detalle_venta"),
    path("ventas/", views.lista_ventas, name="lista_ventas"),
