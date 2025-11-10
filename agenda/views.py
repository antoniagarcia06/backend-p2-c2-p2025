from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from .models import Contacto
from .forms import ContactoForm

@csrf_protect
def lista_contactos(request):
    busqueda = request.GET.get('q', '')
    contactos = Contacto.objects.all()
    if busqueda:
        contactos = contactos.filter(nombre__icontains=busqueda) | contactos.filter(email__icontains=busqueda)
    paginator = Paginator(contactos, 5)
    page = request.GET.get('page')
    contactos = paginator.get_page(page)
    return render(request, 'agenda/lista_contactos.html', {'contactos': contactos, 'busqueda': busqueda})

@csrf_protect
def nuevo_contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contacto creado exitosamente.")
            return redirect('lista_contactos')
        messages.error(request, "Error al crear el contacto. Verifique los datos.")
    else:
        form = ContactoForm()
    return render(request, 'agenda/nuevo_contacto.html', {'form': form})

@csrf_protect
def editar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            messages.success(request, "Contacto actualizado correctamente.")
            return redirect('lista_contactos')
        messages.error(request, "Error al actualizar el contacto.")
    else:
        form = ContactoForm(instance=contacto)
    return render(request, 'agenda/editar_contacto.html', {'form': form, 'contacto': contacto})

@csrf_protect
def eliminar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        contacto.delete()
        messages.success(request, "Contacto eliminado correctamente.")
        return redirect('lista_contactos')
    return render(request, 'agenda/eliminar_contacto.html', {'contacto': contacto})

@csrf_protect
def buscar_contacto(request):
    busqueda = request.GET.get('q', '')
    contactos = Contacto.objects.filter(nombre__icontains=busqueda) | Contacto.objects.filter(email__icontains=busqueda)
    return render(request, 'agenda/buscar_contacto.html', {'contactos': contactos, 'busqueda': busqueda})
