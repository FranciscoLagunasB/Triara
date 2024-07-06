from django.urls import path
from .views import ContactoAPIView

urlpatterns = [
    path('contactos/', ContactoAPIView.as_view(), name='contacto-list'),
    path('contactos/<int:pk>/', ContactoAPIView.as_view(), name='contacto-detail'),
]