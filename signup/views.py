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
class SignUpView(APIView):

    def get(self, request):
        #Muestra los usuarios
        usuarios = list(Usuario.objects.values())
        if len(usuarios) > 0:
            datos = {'Message': "Success GET", 'Usuarios': usuarios}
        else:
            datos = {'Message': "Usuarios not found..."}
        return Response(datos)

    def post(self, request):
        #Captura los datos enviados por el frontend y realiza el registro del usuario
        print(request.body)
        jd = json.loads(request.body)
        usuarios = list(Usuario.objects.values())
        id = 0 #Hallar siguiente Id
        repetido = False #Saber si hay un correo o usuario repetido
        for usr in usuarios: 
            if usr['IdUsuario'] > id: id = usr['IdUsuario']
            if usr['Email'] == jd["Email"] or usr['Usuario'] == jd["Usuario"]: repetido = True
            id += 1
        if (not repetido):
            Usuario.objects.create(IdUsuario = id, Email = jd["Email"], Usuario = jd["Usuario"], Contrasena = jd["Contrasena"])
            datos = {'Message': 'Success POST', 'Signup': 'True', "ID": id}
        else:
            datos = {'Message': 'Usuario repetido', 'Signup': 'False'}
        
        return JsonResponse(datos)

    def put(self, request):
        pass

    def delete(self, request):
        pass


class RegistroUsuario(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class RegistroUsuarioUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer