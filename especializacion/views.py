#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from home_api.models import Usuario
from home_api.models import Especialidad
from home_api.models import Pregunta
from home_api.models import Examen
from home_api.models import ExamenesXUsuario
from home_api.models import PreguntasXExamenes
from home_api.models import PreguntasXExamenXUsuario
from formulario.serializers import PreguntaSerializer
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import json

# Create your views here.


class EspecializacionView(APIView):

    def get(self, request, id=0):
        #envia especializaciones
        especializaciones = list(Especialidad.objects.values())
        if len(especializaciones) > 0:
            datos = {'Message': "Success GET", 'Especializaciones': especializaciones}
        else:
            datos = {'Message': "Especializaciones not found..."}
        return Response(datos)

    def post(self, request):
        #Captura los datos enviados por el frontend y envía un mensaje de autorización
        print(request.body)
        jd = json.loads(request.body)
        datos = {'Message': 'Que chimba sog'}
        
        return JsonResponse(datos)