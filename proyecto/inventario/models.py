from django.db import models

class Cliente(models.Model):
    nombre= models.CharField(max_length=100)
    rut= models.CharField(max_length=12, unique=True)
    email = models.EmailField(blank=True, null=True)       

    def __str__(self):
        return  f"{self.rut} - {self.nombre if self.nombre else 'Cliente ocasional'}"
 
class Venta(models.Model):
    cliente= models.ForeignKey(Cliente, on_delete=  models.SET_NULL, null=True, blank=True)
    fecha= models.DateTimeField(auto_now_add=True)
    def _str_(self):
        return f"Venta {self.id} - {self.fecha.strftime('%Y-%m-%d')}"
    
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    def subtotal(self):
        return self.cantidad * self.precio_unitario
