from django import forms
from django.core.exceptions import ValidationError
from .models import Producto, Cliente
import re
def clean_rut_format(rut: str) -> str:
    rut = rut.upper()
    rut = rut.replace('.', '').replace(' ', '')
    rut = rut.replace('‐', '-').replace('—', '-')
    if '-' not in rut and len(rut) > 1:
        rut, dv = rut[:-1], rut[-1]
        return f"{rut}-{dv}"
    return rut

def validar_rut(rut: str) -> bool:
    rut = clean_rut_format(rut)
    if '-' not in rut:
        return False
    num, dv = rut.split('-')
    if not num.isdigit():
        return False
    reversed_digits = map(int, reversed(num))
    factors = [2,3,4,5,6,7]
    s = 0
    factor_index = 0
    for d in reversed_digits:
        s += d * factors[factor_index]
        factor_index = (factor_index + 1) % len(factors)
    mod = 11 - (s % 11)
    if mod == 11:
        expected = '0'
    elif mod == 10:
        expected = 'K'
    else:
        expected = str(mod)
    return dv == expected

def validar_rut_o_levantar_error(valor):
    rut = clean_rut_format(valor)
    if not validar_rut(rut):
        raise ValidationError("RUT inválido.")
    return rut
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'codigo', 'descripcion', 'precio', 'cantidad']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows':3}),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise ValidationError("El precio debe ser superior a 1")
        return precio

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad < 0:
            raise ValidationError("La cantidad no puede ser menor a 0")
        return cantidad


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'email']

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        rut_norm = clean_rut_format(rut)
        if not validar_rut(rut_norm):
            raise ValidationError("RUT inválido.")
        return rut_norm


class VentaForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False, empty_label="-- Ninguno --")
    rut_boleta = forms.CharField(max_length=12, required=True, label="RUT para boleta")
    guardar_cliente = forms.BooleanField(required=False, initial=False, label="Guardar como cliente habitual")
    nombre_cliente = forms.CharField(max_length=200, required=False)
    email_cliente = forms.EmailField(required=False)

    def clean_rut_boleta(self):
        rut = self.cleaned_data.get('rut_boleta')
        rut_norm = clean_rut_format(rut)
        if not validar_rut(rut_norm):
            raise ValidationError("RUT inválido.")
        return rut_norm

    def clean(self):
        cleaned = super().clean()
        guardar = cleaned.get('guardar_cliente')
        cliente = cleaned.get('cliente')
        nombre = cleaned.get('nombre_cliente')
        if guardar and not cliente and not nombre:
            raise ValidationError("Ingrese el nombre para guardar a cliente como habitual")
        return cleaned


class VentaItemForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), required=True)
    cantidad = forms.IntegerField(min_value=1, required=True)

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0.")
        return cantidad
