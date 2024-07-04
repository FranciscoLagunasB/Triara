from django.contrib import admin
from django.urls import path, include

from Contactos.views import ContactoListAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Contactos.url')),
    # path('api/contactos/', ContactoListAPIView.as_view(), name='contacto-list'),

]
