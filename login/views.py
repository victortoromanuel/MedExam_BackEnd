#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from home_api.models import Especialidad
from home_api.models import Usuario
from signup.serializers import UsuarioSerializer
from django.views import View
from django.http import JsonResponse
import json

# Create your views here.
class LoginView(APIView):

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
        print(type(jd))
        usuario = Usuario.objects.filter(Email = jd['Email'], Contrasena = jd['Contrasena']) | Usuario.objects.filter(Usuario = jd['Email'], Contrasena = jd['Contrasena'])
        usuario = list(usuario)
        if len(usuario) > 0:
            datos = {'Message': 'Success POST', 'Login': "True", 'ID': usuario[0].IdUsuario}
        else:
            datos = {'Message': "User not found...", 'Login': "False"}
        return JsonResponse(datos)

    def put(self, request):
        pass

    def delete(self, request):
        pass
