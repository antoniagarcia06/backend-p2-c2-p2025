from django.contrib import admin
from .models import Producto, Cliente, Venta, VentaItem

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'precio', 'cantidad')
    search_fields = ('codigo', 'nombre')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'email')
    search_fields = ('rut', 'nombre')

class VentaItemInline(admin.TabularInline):
    model = VentaItem
    readonly_fields = ('precio_unitario',)
    extra = 0

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'rut_boleta', 'cliente', 'fecha', 'total')
    inlines = [VentaItemInline]
    readonly_fields = ('total', 'fecha')
