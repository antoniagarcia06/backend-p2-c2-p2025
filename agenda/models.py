from django.db import models
from django.core.validators import RegexValidator, EmailValidator

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Etiquetas"

    def __str__(self):
        return self.nombre


class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True, validators=[EmailValidator()])
    direccion= models.CharField(max_length=255, blank=True)
    telefono = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{7,15}$',
                message="El número debe tener entre 7 y 15 dígitos y puede iniciar con +."
            )
        ]
    )
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.email})"
