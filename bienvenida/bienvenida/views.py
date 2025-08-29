from django.http import HttpResponse 

from django.shortcuts import render
from . import models

def inicio (request):
    return HttpResponse ('hola mundo, desde django')

def mostrar_bienvenida(rquest):
    tu_nombre ="Antonia garcia"
    return HttpResponse (f'¡Bienvenidos a mi primera app Django , antonia garcia ')

def lista_productos (request):
    productos = models.Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos}) 