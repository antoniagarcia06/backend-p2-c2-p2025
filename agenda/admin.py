from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Contacto, Etiqueta

@admin.action(description="Exportar contactos a CSV")
def exportar_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contactos.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Email', 'Teléfono', 'Etiquetas'])
    for c in queryset:
        etiquetas = ", ".join(e.nombre for e in c.etiquetas.all())
        writer.writerow([c.nombre, c.email, c.telefono, etiquetas])
    return response

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'correo', 'telefono', 'creado_en']  # Cambiar 'email' por 'correo'
    search_fields = ('nombre', 'email')
    actions = [exportar_csv]

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)
