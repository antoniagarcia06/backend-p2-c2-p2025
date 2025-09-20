from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Producto, Cliente, Venta, DetalleVenta
from .forms import ProductoForm, ClienteForm

def lista_productos(request):
    productos= Producto.objects.all()
    return render(request, "inventario/lista_productos.html", {"productos":productos})

def nuevo_producto(request):
    if request.method =="POST":
        form =ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_productos")
        else:
            form= ProductoForm
        return render(request, "inventario/nuevo_producto.html", {"form":form})

def editar_producto(request, id):
    producto= get_object_or_404(Producto, id=id)
    if request.method =="POST":
        form= ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("lista_productos")
    else:
        form =ProductoForm(instance=producto)
    return render(request, "inventario/editar_producto.html", {"form":form, "producto":producto})

def eliminar_producto(request, id):
    producto= get_object_or_404(Producto, id=id)
    if request.method == "POST":
        producto.delete()
    return render(request, "inventario/eliminar_producto.html",{"profucto":producto} )


def lista_ventas(request):
    ventas= Venta.objects.all().order_by("-fecha")
    return render(request, "inventario/lista_ventas.html", {"ventas":ventas})


def registrar_venta(request):
    if request.method == "POST":
        cliente_form = ClienteForm(request.POST)
        if cliente_form.is_valid():
            data = cliente_form.cleaned_data
            cliente, created = Cliente.objects.get_or_create(
                rut=data['rut'],
                defaults={
                    "nombre": data.get('nombre'),
                    "correo": data.get('correo'),
                    "telefono": data.get('telefono'),
                    "habitual": data.get('habitual', False)
                }
            )
            venta = Venta.objects.create(cliente=cliente)

            productos_ids = request.POST.getlist("producto") 
            for pid in productos_ids:
                cantidad = int(request.POST.get(f"cantidad_{pid}", "1"))
                producto = get_object_or_404(Producto, id=pid)
                if producto.cantidad < cantidad:
                    venta.delete()
                    messages.error(request, f"Stock insuficiente para {producto.nombre}")
                    return redirect("registrar_venta")
                DetalleVenta.objects.create(venta=venta, producto=producto, cantidad=cantidad)
                producto.cantidad -= cantidad
                producto.save()

            messages.success(request, f"Venta registrada (#{venta.id})")
            return redirect("detalle_venta", id=venta.id)
        else:
            messages.error(request, "Corrige los errores del formulario de cliente.")
    else:
        cliente_form = ClienteForm()

    productos = Producto.objects.all()
    return render(request, "inventario/registrar_venta.html", {"cliente_form": cliente_form, "productos": productos})


def detalle_venta(request, id):
    venta = Venta.objects.get(id=id)
    return render(request, "inventario/detalle_venta.html", {"venta": venta})
