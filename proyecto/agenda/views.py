from django.shortcuts import render, get_object_or_404, redirect
from .models import Contacto
from .forms import ContactoForm
from django.db.models import Q

# Lista todos los contactos
def lista_contactos(request):
    query = request.GET.get('q', '')  # captura el parámetro 'q'
    if query:
        contactos = Contacto.objects.filter(Q(nombre__icontains=query) | Q(correo__icontains=query))
    else:
        contactos = Contacto.objects.all()
    return render(request, 'agenda/lista_contactos.html', {'contactos': contactos, 'query': query})


# Crear un nuevo contacto
def nuevo_contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_contactos')
    else:
        form = ContactoForm()
    return render(request, 'agenda/nuevo_contacto.html', {'form': form})

# Editar contacto
def editar_contacto(request, id):
    contacto = get_object_or_404(Contacto, id=id)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('lista_contactos')
    else:
        form = ContactoForm(instance=contacto)
    return render(request, 'agenda/editar_contacto.html', {'form': form})

# Aqui se eliminaran los contactos 
def eliminar_contacto(request, id):
    contacto = get_object_or_404(Contacto, id=id)
    if request.method == 'POST':
        contacto.delete()
        return redirect('lista_contactos')
    return render(request, 'agenda/eliminar_contacto.html', {'contacto': contacto})

# Opcion para buscar contacto ya sea por correo o nombre
def buscar_contacto(request):
    query = request.GET.get('q', '')
    contactos = Contacto.objects.filter(Q(nombre__icontains=query) | Q(correo__icontains=query))
    return render(request, 'agenda/buscar_contacto.html', {'contactos': contactos, 'query': query})
