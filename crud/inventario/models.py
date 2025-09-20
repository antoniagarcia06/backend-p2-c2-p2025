from django.db import models

from django.core.validators import MinValueValidator

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True)  
    nombre = models.CharField(max_length=100, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    habitual = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.rut} - {self.nombre if self.nombre else 'Cliente Ocasional'}"


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.detalles.all())

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.rut}"



class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name="detalles", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
