from django import forms
from .models import Cliente, Venta, DetalleVenta, Producto

class ClienteForm(forms.ModelForm):
    class Meta:
        model= Cliente
        fields=['nombre', 'rut', 'email']

class VentaForm(forms.Form):
    rut= forms.CharField(label='RUT Cliente', max_length=12)
    clienteHabitual=forms.BooleanField(required=False, label='¿Es cliente habitual?')



class DetalleVentaForm(forms.Form):
    producto= forms.CharField(queryset=Producto.objects.filter(cantidad_gt=0))
    cantidad =forms.IntegerField(min_value=1)