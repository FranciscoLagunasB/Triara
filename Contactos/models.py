from django.db import models

class Contacto(models.Model):
    contacto_PK = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    alias = models.CharField(max_length=50)
    foto = models.TextField(blank=True, null=True)

class Correo(models.Model):
    correo_PK = models.AutoField(primary_key=True)
    contacto = models.ForeignKey(Contacto, related_name='correos', on_delete=models.CASCADE)
    correo = models.EmailField()

class Telefono(models.Model):
    telefono_PK = models.AutoField(primary_key=True)
    contacto = models.ForeignKey(Contacto, related_name='telefonos', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    numero = models.CharField(max_length=20)

class Direccion(models.Model):
    direccion_PK = models.AutoField(primary_key=True)
    contacto = models.ForeignKey(Contacto, related_name='direcciones', on_delete=models.CASCADE)
    calle = models.CharField(max_length=100)
    numero_exterior = models.CharField(max_length=10)
    colonia = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
