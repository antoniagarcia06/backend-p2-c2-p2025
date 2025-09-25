from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.forms import formset_factory
from .models import Producto, Cliente, Venta, VentaItem
from .forms import ProductoForm, ClienteForm, VentaForm, VentaItemForm

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/lista_productos.html', {'productos': productos})

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'inventario/detalle_producto.html', {'producto': producto})

def nuevo_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado con exito')
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'inventario/nuevo_producto.html', {'form': form})

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado.')
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/editar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado.')
        return redirect('lista_productos')
    return render(request, 'inventario/eliminar_producto.html', {'producto': producto})

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'inventario/lista_clientes.html', {'clientes': clientes})

def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente guardado exitosamente.')
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'inventario/nuevo_cliente.html', {'form': form})

def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'inventario/lista_ventas.html', {'ventas': ventas})

def detalle_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    return render(request, 'inventario/detalle_venta.html', {'venta': venta})

def nueva_venta(request):
    VentaItemFormSet = formset_factory(VentaItemForm, extra=5)  
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        formset = VentaItemFormSet(request.POST)
        if venta_form.is_valid() and formset.is_valid():
            items_data = [f for f in formset.cleaned_data if f and f.get('producto') and f.get('cantidad')]
            if not items_data:
                messages.error(request, "Debes ingresar al menos 1 cantidad")
                return render(request, 'inventario/nueva_venta.html', {'venta_form': venta_form, 'formset': formset})
            try:
                with transaction.atomic():
                    cliente_obj = None
                    cliente_sel = venta_form.cleaned_data.get('cliente')
                    rut_boleta = venta_form.cleaned_data.get('rut_boleta')
                    guardar_cliente = venta_form.cleaned_data.get('guardar_cliente')
                    nombre_cliente = venta_form.cleaned_data.get('nombre_cliente')
                    email_cliente = venta_form.cleaned_data.get('email_cliente')

                    if cliente_sel:
                        cliente_obj = cliente_sel
                        rut_boleta = cliente_obj.rut  
                    elif guardar_cliente:
                        cliente_obj, created = Cliente.objects.get_or_create(
                            rut=rut_boleta,
                            defaults={'nombre': nombre_cliente or '', 'email': email_cliente or ''}
                        )
                        if not created:
                            if nombre_cliente:
                                cliente_obj.nombre = nombre_cliente
                            if email_cliente:
                                cliente_obj.email = email_cliente
                            cliente_obj.save()
                    venta = Venta.objects.create(cliente=cliente_obj, rut_boleta=rut_boleta, total=Decimal('0.00'))

                    total = Decimal('0.00')
                    for item in items_data:
                        producto = Producto.objects.select_for_update().get(pk=item['producto'].pk)
                        cantidad = int(item['cantidad'])
                        if producto.cantidad < cantidad:
                            raise ValueError(f"No hay stock suficiente para {producto.nombre}. Stock actual: {producto.cantidad}")
                    for item in items_data:
                        producto = Producto.objects.select_for_update().get(pk=item['producto'].pk)
                        cantidad = int(item['cantidad'])
                        precio_unitario = producto.precio

                        VentaItem.objects.create(
                            venta=venta,
                            producto=producto,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario
                        )

                        producto.cantidad -= cantidad
                        producto.save()

                        total += (precio_unitario * cantidad)

                    venta.total = total
                    venta.save()

                    messages.success(request, f"Venta registrada correctamente. Total: ${venta.total}")
                    return redirect('detalle_venta', id=venta.id)

            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Error al registrar la venta: {e}")
        else:
            messages.error(request, "Hay errores en el formulario. Revise los datos.")
    else:
        venta_form = VentaForm()
        formset = VentaItemFormSet()

    return render(request, 'inventario/nueva_venta.html', {
        'venta_form': venta_form,
        'formset': formset
    })
