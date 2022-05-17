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
import json

# Create your views here.
class TableView(APIView):

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
                   'Examenes': []}
        cnt = 0
        exam = []
        for eu in examenesXUsuario:
            preguntasCorrectasGen += eu.PreguntasCorrectas
            totalPreguntasGen += eu.TotalPreguntas
            examen = [{'IdExamenXUsuario': eu.IdExamenesXUsuario,
                      'Nombre': 'Examen ' + eu.IdExamen.Nombre,
                      'PreguntasCorrectas': eu.PreguntasCorrectas,
                      'TotalPreguntas': eu.TotalPreguntas}]
            key = 'Examen'
            exam.append(examen)
            cnt += 1
        Message['TotalExamenes'] = totalExamenes
        Message['PreguntasCorrectasGeneral'] = preguntasCorrectasGen
        Message['TotalPreguntasGeneral'] = totalPreguntasGen
        Message['Examenes'] = exam
        return Message

    def countCorrectAnswers(self, preguntasRespondidas):
        c = 0
        for pr in preguntasRespondidas:
            for r in pr:
                if r['RespuestaSeleccionada'] == r['RespuestaCorrecta']:
                    c += 1
        return c

    def setPuntaje(self, idUsuario):
        usuario = Usuario.objects.filter(IdUsuario = idUsuario)
        examenesXUsuario = ExamenesXUsuario.objects.filter(IdUsuario = usuario[0])
        for eu in examenesXUsuario:
            preguntasXExamenXUsuarios = PreguntasXExamenXUsuario.objects.filter(IdUsuario = usuario[0], IdExamenesXUsuario = eu)
            preguntasRespondidas = []
            for peu in preguntasXExamenXUsuarios:
                pregunta = Pregunta.objects.filter(IdPregunta = peu.IdPregunta.IdPregunta)
                serializer = PreguntaSerializer(pregunta, many=True)
                newData = list(serializer.data)
                newData[0].update({'RespuestaSeleccionada': peu.RespuestaSeleccionada})
                preguntasRespondidas.append(newData)
            nCorrectas = self.countCorrectAnswers(preguntasRespondidas)
            updateEU = ExamenesXUsuario.objects.filter(IdExamenesXUsuario = eu.IdExamenesXUsuario)
            updateEU.update(PreguntasCorrectas = nCorrectas, TotalPreguntas = len(preguntasXExamenXUsuarios))
        return

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
    
    def deletePreguntasSinExamen(self, idUsuario):
        usuario = Usuario.objects.filter(IdUsuario = idUsuario)
        preguntasXExamenXUsuarios = PreguntasXExamenXUsuario.objects.filter(IdUsuario = usuario[0])
        """
        for peu in preguntasXExamenXUsuarios:
            print(peu.IdExamenesXUsuario.IdExamenesXUsuario)
            examen = ExamenesXUsuario.objects.filter(IdExamenesXUsuario = peu.IdExamenesXUsuario.IdExamenesXUsuario)
            print(examen, len(examen))
            if len(examen) == 0:
                PreguntasXExamenXUsuario.objects.filter(IdPreguntasXExamenXUsuario = peu.IdPreguntasXExamenXUsuario).delete()
        """
        for i in range(350):
            examen = ExamenesXUsuario.objects.filter(IdExamenesXUsuario = i)
            #print(examen)
            preguntasXExamenXUsuarios = PreguntasXExamenXUsuario.objects.filter(IdExamenesXUsuario = i)
            if not examen.exists():
                #print("Algo", preguntasXExamenXUsuarios)
                for peu in preguntasXExamenXUsuarios:
                    #print(peu)
                    PreguntasXExamenXUsuario.objects.filter(IdPreguntasXExamenXUsuario = peu.IdPreguntasXExamenXUsuario).delete()
        return

    def get(self, request):
        #Muestra los usuarios
        usuarios = list(Usuario.objects.values())
        if len(usuarios) > 0:
            datos = {'Message': "Success GET"}
        else:
            datos = {'Message': "Usuarios not found..."}
        return Response(datos)

    def post(self, request):
        #Captura los datos enviados por el frontend y envía la información de los resultados de los exámenes por usuario
        print(request.body)
        jd = json.loads(request.body)
        self.deleteExamenNull(int(jd['userId']))
        self.deleteExamenIncompleto(int(jd['userId']))
        #self.setPuntaje(int(jd['userId'])) 
        #self.deletePreguntasSinExamen(int(jd['userId']))
        datos = self.getExamenesXUsuario(int(jd['userId']))

        return Response(datos)