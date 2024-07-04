from django.urls import path
from .views import ContactoListAPIView

urlpatterns = [
    path('contactos/', ContactoListAPIView.as_view(), name='contacto-list'),
    # Otras URLs de la app Contactos si las tienes
]