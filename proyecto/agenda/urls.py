from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_contactos, name='lista_contactos'),
    path('contacto/nuevo/', views.nuevo_contacto, name='nuevo_contacto'),
    path('contacto/editar/<int:id>/', views.editar_contacto, name='editar_contacto'),
    path('contacto/eliminar/<int:id>/', views.eliminar_contacto, name='eliminar_contacto'),
    path('buscar/', views.buscar_contacto, name='buscar_contacto'),
]
