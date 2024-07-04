from rest_framework import generics
from .models import Contacto
from .serializers import ContactoSerializer

class ContactoListAPIView(generics.ListAPIView):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer
