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

class DashboardView(APIView):

    def getExamenesXUsuario(self, idUsuario):
        totalExamenes = 0
        preguntasCorrectasGen = 0
        totalPreguntasGen = 0
        usuario = Usuario.objects.filter(IdUsuario = idUsuario)
        examenesXUsuario = ExamenesXUsuario.objects.filter(IdUsuario = usuario[0])
        totalExamenes = len(examenesXUsuario)
        Message = {'IdUsuario': idUsuario, 
                   'TotalExamenes': 0,
                   'PreguntasCorrectasGeneral': 0,
                   'TotalPreguntasGeneral': 0,
                   'Pastel': [],
                   }
        for eu in examenesXUsuario:
            preguntasCorrectasGen += eu.PreguntasCorrectas
            totalPreguntasGen += eu.TotalPreguntas
        Message['TotalExamenes'] = totalExamenes
        Message['PreguntasCorrectasGeneral'] = preguntasCorrectasGen
        Message['TotalPreguntasGeneral'] = totalPreguntasGen
        Message['Pastel'].append(preguntasCorrectasGen)
        Message['Pastel'].append(totalPreguntasGen)
        return Message

    def deleteExamenNull(self, idUsuario):
        usuario = Usuario.objects.filter(IdUsuario = idUsuario)
        examenesXUsuario = ExamenesXUsuario.objects.filter(IdUsuario = usuario[0])
        for eu in examenesXUsuario:
            if (eu.PreguntasCorrectas == None and eu.TotalPreguntas == None) or eu.TotalPreguntas == 0:
                preguntasXExamenXUsuarios = PreguntasXExamenXUsuario.objects.filter(IdUsuario = usuario[0], IdExamenesXUsuario = eu)
                for peu in preguntasXExamenXUsuarios:
                    PreguntasXExamenXUsuario.objects.filter(IdPreguntasXExamenXUsuario = peu.IdPreguntasXExamenXUsuario).delete()
                ExamenesXUsuario.objects.filter(IdExamenesXUsuario = eu.IdExamenesXUsuario).delete()
        return

    def deleteExamenIncompleto(self, idUsuario):
        usuario = Usuario.objects.filter(IdUsuario = idUsuario)
        examenesXUsuario = ExamenesXUsuario.objects.filter(IdUsuario = usuario[0])
        for eu in examenesXUsuario:
            #Quitar el total preguntas != 20 del if cuando se tengan mas de 50 preguntas
            if eu.TotalPreguntas != 5 and eu.TotalPreguntas != 20 and eu.TotalPreguntas != 30 and eu.TotalPreguntas != 40 and eu.TotalPreguntas != 50: 
                preguntasXExamenXUsuarios = PreguntasXExamenXUsuario.objects.filter(IdUsuario = usuario[0], IdExamenesXUsuario = eu)
                for peu in preguntasXExamenXUsuarios:
                    PreguntasXExamenXUsuario.objects.filter(IdPreguntasXExamenXUsuario = peu.IdPreguntasXExamenXUsuario).delete()
                ExamenesXUsuario.objects.filter(IdExamenesXUsuario = eu.IdExamenesXUsuario).delete()
        return

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
        self.deleteExamenNull(int(jd['userId']))
        self.deleteExamenIncompleto(int(jd['userId']))
        datos = self.getExamenesXUsuario(int(jd['userId']))
        
        return JsonResponse(datos)