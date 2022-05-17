#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from home_api.models import Especialidad
from home_api.models import Usuario
from django.views import View
from django.http import JsonResponse
import json

# Create your views here.
class UserView(APIView):

    def get(self, request):
        #Muestra los usuarios
        usuarios = list(Usuario.objects.values())
        if len(usuarios) > 0:
            datos = {'Message': "Success GET"}
        else:
            datos = {'Message': "Usuarios not found..."}
        return Response(datos)

    def post(self, request):
        #Captura los datos enviados por el frontend y realiza el registro del usuario
        print(request.body)
        jd = json.loads(request.body)
        usuario = Usuario.objects.filter(IdUsuario = int(jd['userId']))
        if jd["POST"] == False:
            datos = {'IdUsuario': usuario[0].IdUsuario,
                     'Nombre': usuario[0].Nombre,
                     'Email': usuario[0].Email,
                     'Usuario': usuario[0].Usuario,
                     'Edad': usuario[0].Edad
                    }
        else:
            if jd['Nombre'] != None:
                usuario.update(Nombre = jd['Nombre'])
            if jd['Edad'] != None:
                usuario.update(Edad = jd['Edad'])
            if jd['Contrasena'] != None:
                usuario.update(Contrasena = jd['Contrasena'])
            datos = {'Message': 'Se han actualizado los datos'}
        return Response(datos)