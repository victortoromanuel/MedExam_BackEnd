#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from home_api.models import Especialidad
from home_api.models import Usuario
from signup.serializers import UsuarioSerializer
from django.views import View
from django.http import JsonResponse
from django.core.mail import send_mail
import random
from random import choice, randint
import json

def generarContrasena():
    contrasena = ''
    characters = 'abcdefghijklmnopqrstuvwxyz'
    characters += characters.upper()
    characters += '-_+!@#$%&*^()'
    characters += '0123456789'
    characters = list(characters)
    for c in range(10):
        contrasena += random.choice(characters)
    return contrasena


# Create your views here.
class ForgotpswView(APIView):

    def get(self, request, id=0):
        #Muestra los usuarios
        usuarios = list(Usuario.objects.values())
        if len(usuarios) > 0:
            datos = {'Message': "Success GET", 'Usuarios': usuarios}
        else:
            datos = {'Message': "Usuarios not found..."}
        return Response(datos)

    def post(self, request):
        #Captura los datos enviados por el frontend y envía un mensaje de autorización
        print(request.body)
        jd = json.loads(request.body)
        usuario = list(Usuario.objects.filter(Email = jd['Email']))
        if len(usuario) > 0:
            contrasenarNueva = generarContrasena()
            mensaje = "¡Hola! aquí está tu nueva contraseña. Podrás cambiarla cuando desees." + '\n\n' + 'Contraseña nueva: ' + contrasenarNueva
            try:
                send_mail(
                    'Nueva constraseña MedExam',
                    mensaje,
                    'medexamemail@gmail.com',
                    [usuario[0].Email],
                    fail_silently=False,
                )
                Usuario.objects.filter(IdUsuario = usuario[0].IdUsuario).update(Contrasena = contrasenarNueva)
                datos = {'Message': 'Success POST', 'Exist': "True"}
            except:
                print("Algo ocurrió y no se envió el email ni se cambió la contraseña.")
                datos = {'Message': 'Success POST but failed sending mail', 'Exist': "True"}
            
        else:
            datos = {'Message': "User not found...", 'Exist': "False"}
        return JsonResponse(datos)

    def put(self, request):
        pass

    def delete(self, request):
        pass
