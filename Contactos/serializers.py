from rest_framework import serializers
from .models import Contacto, Correo, Telefono, Direccion

class CorreoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correo
        fields = ['id', 'correo']

class TelefonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefono
        fields = ['id', 'tipo', 'numero']

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ['id', 'calle', 'numero_exterior', 'colonia', 'ciudad', 'estado', 'pais', 'codigo_postal']

class ContactoSerializer(serializers.ModelSerializer):
    correos = CorreoSerializer(many=True, read_only=True)
    telefonos = TelefonoSerializer(many=True, read_only=True)
    direcciones = DireccionSerializer(many=True, read_only=True)

    class Meta:
        model = Contacto
        fields = ['id', 'nombres', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'alias', 'foto', 'correos', 'telefonos', 'direcciones']
