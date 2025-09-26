from django import forms
from .models import Contacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'telefono', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre completo'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección'}),
        }
