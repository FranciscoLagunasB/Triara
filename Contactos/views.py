import json
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Contacto, Correo, Telefono, Direccion
from .serializers import ContactoSerializer
from django.core.serializers.json import DjangoJSONEncoder


class ContactoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Contacto.objects.all()
        serializer = ContactoSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        ultimo_contacto = Contacto.objects.last()
        if ultimo_contacto:
            siguiente_contacto_pk = ultimo_contacto.contacto_PK + 1
        else:
            siguiente_contacto_pk = 1

        # Guardar el contacto
        nuevo_contacto = Contacto.objects.create(
            contacto_PK = siguiente_contacto_pk,
            nombres=data['nombres'],
            apellido_paterno=data['apellido_paterno'],
            apellido_materno=data['apellido_materno'],
            fecha_nacimiento=data['fecha_nacimiento'],
            alias=data['alias'],
        )

        if 'foto' in data and data['foto']:
            nuevo_contacto.foto = data['foto']
            nuevo_contacto.save()


        for correo in data['correos']:
            Correo.objects.create(contacto=nuevo_contacto, correo=correo)

        # Guardar teléfonos
        for telefono in data['telefonos']:
            Telefono.objects.create(
                contacto=nuevo_contacto,
                tipo=telefono['tipo'],
                numero=telefono['numero']
            )

        # Guardar direcciones
        for direccion in data['direcciones']:
            Direccion.objects.create(
                contacto=nuevo_contacto,
                calle=direccion['calle'],
                numero_exterior=direccion['numero_exterior'],
                colonia=direccion['colonia'],
                ciudad=direccion['ciudad'],
                estado=direccion['estado'],
                pais=direccion['pais'],
                codigo_postal=direccion['codigo_postal']
            )
        # Serializar el nuevo contacto creado
        serializer = ContactoSerializer(nuevo_contacto)

        # Devolver registro creado
        return JsonResponse({'status': True, 'data': serializer.data}, status=201)
    
    def put(self, request, pk):
        try:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Error en el JSON de la solicitud'}, status=400)

            try:
                contacto = Contacto.objects.get(contacto_PK=pk)
            except Contacto.DoesNotExist:
                return JsonResponse({'message': 'Contacto no encontrado'}, status=404)
        
            contacto.nombres = data['nombres']
            contacto.apellido_paterno = data['apellido_paterno']
            contacto.apellido_materno = data['apellido_materno']
            contacto.fecha_nacimiento = data['fecha_nacimiento']
            contacto.alias = data['alias']
            if 'foto' in data and data['foto']:
                contacto.foto = data['foto']

            contacto.save()

            # Actualizar correos
            correos_actualizados = []
            for correo_data in data.get('correos', []):
                if 'correo_PK' in correo_data:
                    try:
                        correo_existente = Correo.objects.get(correo_PK=correo_data['correo_PK'], contacto=contacto)
                        correo_existente.correo = correo_data['correo']
                        correo_existente.save()
                        correos_actualizados.append({
                            'correo_PK': correo_existente.correo_PK,
                            'contacto': correo_existente.contacto.contacto_PK,
                            'correo': correo_existente.correo
                        })
                    except Correo.DoesNotExist:
                        pass  # Manejar el error o ignorar si el correo no existe
                else:
                    nuevo_correo = Correo.objects.create(contacto=contacto, correo=correo_data['correo'])
                    correos_actualizados.append({
                        'correo_PK': nuevo_correo.correo_PK,
                        'contacto': nuevo_correo.contacto.contacto_PK,
                        'correo': nuevo_correo.correo
                    })

            # Eliminar correos que no se enviaron en el formulario
            Correo.objects.filter(contacto=contacto).exclude(correo_PK__in=[c['correo_PK'] for c in correos_actualizados]).delete()

            # Actualizar telefonos
            telefonos_actualizados = []
            for telefono_data in data.get('telefonos', []):
                if 'telefono_PK' in telefono_data:
                    try:
                        telefono_existente = Telefono.objects.get(telefono_PK=telefono_data['telefono_PK'], contacto=contacto)
                        telefono_existente.tipo = telefono_data['tipo']
                        telefono_existente.numero = telefono_data['numero']
                        telefono_existente.save()
                        telefonos_actualizados.append({
                            'telefono_PK': telefono_existente.telefono_PK,
                            'contacto': telefono_existente.contacto.contacto_PK,
                            'tipo': telefono_existente.tipo,
                            'numero': telefono_existente.numero
                        })
                    except Telefono.DoesNotExist:
                        pass  # Manejar el error o ignorar si el teléfono no existe
                else:
                    nuevo_telefono = Telefono.objects.create(contacto=contacto, tipo=telefono_data['tipo'], numero=telefono_data['numero'])
                    telefonos_actualizados.append({
                        'telefono_PK': nuevo_telefono.telefono_PK,
                        'contacto': nuevo_telefono.contacto.contacto_PK,
                        'tipo': nuevo_telefono.tipo,
                        'numero': nuevo_telefono.numero
                    })

            # Eliminar telefonos que no se enviaron en el formulario
            Telefono.objects.filter(contacto=contacto).exclude(telefono_PK__in=[t['telefono_PK'] for t in telefonos_actualizados]).delete()

            # Actualizar direcciones
            direcciones_actualizadas = []
            for direccion_data in data.get('direcciones', []):
                if 'direccion_PK' in direccion_data:
                    try:
                        direccion_existente = Direccion.objects.get(direccion_PK=direccion_data['direccion_PK'], contacto=contacto)
                        direccion_existente.calle = direccion_data['calle']
                        direccion_existente.numero_exterior = direccion_data['numero_exterior']
                        direccion_existente.colonia = direccion_data['colonia']
                        direccion_existente.ciudad = direccion_data['ciudad']
                        direccion_existente.estado = direccion_data['estado']
                        direccion_existente.pais = direccion_data['pais']
                        direccion_existente.codigo_postal = direccion_data['codigo_postal']
                        direccion_existente.save()
                        direcciones_actualizadas.append({
                            'direccion_PK': direccion_existente.direccion_PK,
                            'contacto': direccion_existente.contacto.contacto_PK,
                            'calle': direccion_existente.calle,
                            'numero_exterior': direccion_existente.numero_exterior,
                            'colonia': direccion_existente.colonia,
                            'ciudad': direccion_existente.ciudad,
                            'estado': direccion_existente.estado,
                            'pais': direccion_existente.pais,
                            'codigo_postal': direccion_existente.codigo_postal
                        })
                    except Direccion.DoesNotExist:
                        pass  # Manejar el error o ignorar si la dirección no existe
                else:
                    nueva_direccion = Direccion.objects.create(
                        contacto=contacto,
                        calle=direccion_data['calle'],
                        numero_exterior=direccion_data['numero_exterior'],
                        colonia=direccion_data['colonia'],
                        ciudad=direccion_data['ciudad'],
                        estado=direccion_data['estado'],
                        pais=direccion_data['pais'],
                        codigo_postal=direccion_data['codigo_postal']
                    )
                    direcciones_actualizadas.append({
                        'direccion_PK': nueva_direccion.direccion_PK,
                        'contacto': nueva_direccion.contacto.contacto_PK,
                        'calle': nueva_direccion.calle,
                        'numero_exterior': nueva_direccion.numero_exterior,
                        'colonia': nueva_direccion.colonia,
                        'ciudad': nueva_direccion.ciudad,
                        'estado': nueva_direccion.estado,
                        'pais': nueva_direccion.pais,
                        'codigo_postal': nueva_direccion.codigo_postal
                    })

            # Eliminar direcciones que no se enviaron en el formulario
            Direccion.objects.filter(contacto=contacto).exclude(direccion_PK__in=[d['direccion_PK'] for d in direcciones_actualizadas]).delete()

            # Preparar el JSON de respuesta con los datos actualizados
            data_actualizada = {
                'contacto_PK': contacto.contacto_PK,
                'nombres': contacto.nombres,
                'apellido_paterno': contacto.apellido_paterno,
                'apellido_materno': contacto.apellido_materno,
                'fecha_nacimiento': str(contacto.fecha_nacimiento),
                'alias': contacto.alias,
                'foto': contacto.foto.url if contacto.foto else None,
                'correos': correos_actualizados,
                'telefonos': telefonos_actualizados,
                'direcciones': direcciones_actualizadas
            }

            # Serializar los datos actualizados a JSON
            try:
                serialized_data = json.dumps({'updated': True, 'data': data_actualizada}, cls=DjangoJSONEncoder)
            except TypeError as e:
                return JsonResponse({'error': 'Error al serializar los datos'}, status=500)

            return JsonResponse(json.loads(serialized_data), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


    def delete(self, request, pk):
        try:
            contacto = Contacto.objects.get(contacto_PK=pk)
        except Contacto.DoesNotExist:
            return JsonResponse({'message': 'Error'}, status=404)
        contacto.delete()
        return JsonResponse({'message': 'Contacto eliminado exitosamente'}, status=201)