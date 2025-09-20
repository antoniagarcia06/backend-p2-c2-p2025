from django import forms
from .models import Producto, Cliente
from django.core.exceptions import ValidationError
from utils import validar_rut

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'cantidad']

class ClienteForm (forms.ModelForm):
    class Meta:
        model= Cliente
        fields= ['rut', 'nombre', 'correo', 'telefono', 'habitual']

def clean_rut(self):
    rut= self.cleaned_data.get('rut')
    if not validar_rut(rut):
        raise ValidationError ("El RUT ingresado no es válido, intenta nuevamente.")
    return rut