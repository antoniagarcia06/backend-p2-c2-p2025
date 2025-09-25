from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True) 
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cantidad = models.PositiveIntegerField(default=0)  
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True) 
    nombre = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rut} - {self.nombre or 'Sin nombre'}"


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    rut_boleta = models.CharField(max_length=12) 
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Venta #{self.id} - {self.rut_boleta} - {self.fecha.date()}"

    def calcular_total(self):
        total = Decimal('0.00')
        for it in self.items.all():
            total += it.subtotal()
        self.total = total
        self.save()
        return self.total


class VentaItem(models.Model):
    venta = models.ForeignKey(Venta, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad} => {self.subtotal()}"
