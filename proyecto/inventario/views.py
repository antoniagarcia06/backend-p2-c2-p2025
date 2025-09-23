from django.shortcuts import render
from django.forms import formset_factory
from django.contrib import messages
from .models import Cliente, Venta, DetalleVenta, Producto
from .forms import ClienteForm, VentaForm, DetalleVentaForm



def nueva_venta(reuest):
    DetalleVentaFormSET =
