from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_contactos, name='lista_contactos'),
    path('nuevo/', views.nuevo_contacto, name='nuevo_contacto'),
    path('editar/<int:pk>/', views.editar_contacto, name='editar_contacto'),
    path('eliminar/<int:pk>/', views.eliminar_contacto, name='eliminar_contacto'),
    path('buscar/', views.buscar_contacto, name='buscar_contacto'),
]
