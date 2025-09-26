from django.db import models
from django.core.validators import EmailValidator

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True, validators=[EmailValidator()])
    direccion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.correo}"
