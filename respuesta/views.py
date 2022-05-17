#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from home_api.models import Especialidad
from home_api.models import Usuario
from home_api.models import Pregunta
from home_api.models import Examen
from home_api.models import ExamenesXUsuario
from home_api.models import PreguntasXExamenXUsuario
from formulario.serializers import PreguntaSerializer
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import json

# Create your views here.
class RespuestaView(APIView):

    def createPreguntasXExamenXUsuario(self, idPregunta, idUsuario, idExamenXUsuario, respuestaSeleccionada, respuestaCorrecta):
        #Crea la instancia de la pregunta respondida por el usuario en ese examen y verifica si correctitud
        preguntasXExamenXUsuarios = list(PreguntasXExamenXUsuario.objects.values())
        idPreguntasXExamenXUsuario = len(preguntasXExamenXUsuarios)
        pregunta = Pregunta.objects.filter(IdPregunta = int(idPregunta))
        usuario = Usuario.objects.filter(IdUsuario = int(idUsuario))
        examenXUsuario = ExamenesXUsuario.objects.filter(IdExamenesXUsuario = int(idExamenXUsuario))
        correcta = False
        if respuestaSeleccionada == respuestaCorrecta:
            correcta = True
        PreguntasXExamenXUsuario.objects.create(IdPreguntasXExamenXUsuario = idPreguntasXExamenXUsuario, IdPregunta = pregunta[0], IdUsuario = usuario[0], IdExamenesXUsuario = examenXUsuario[0], RespuestaSeleccionada = respuestaSeleccionada, Correcta = correcta)
        return
    
    def updatePreguntasXExamenXUsuario(self, idPregunta, idExamenXUsuario, respuestaSeleccionada, respuestaCorrecta):
        #Actualiza la respuesta a una pregunta y verifica si correctitud
        examenXUsuario = ExamenesXUsuario.objects.filter(IdExamenesXUsuario = int(idExamenXUsuario))
        pregunta = Pregunta.objects.filter(IdPregunta = int(idPregunta))
        correcta = False
        if respuestaSeleccionada == respuestaCorrecta:
            correcta = True
        preguntasXExamenXUsuarios = PreguntasXExamenXUsuario.objects.filter(IdExamenesXUsuario = examenXUsuario[0], IdPregunta = pregunta[0])
        preguntasXExamenXUsuarios.update(RespuestaSeleccionada = respuestaSeleccionada, Correcta = correcta)
        return
    
    def isAnswered(self, idPregunta, idExamenXUsuario):
        #Retorna True si la pregunta de ese examen ya fue respondida, False de lo contrario
        ans = False
        examenXUsuario = ExamenesXUsuario.objects.filter(IdExamenesXUsuario = int(idExamenXUsuario))
        pregunta = Pregunta.objects.filter(IdPregunta = int(idPregunta))
        preguntasXExamenXUsuarios = PreguntasXExamenXUsuario.objects.filter(IdExamenesXUsuario = examenXUsuario[0], IdPregunta = pregunta[0])
        if len(preguntasXExamenXUsuarios) > 0:
            ans = True
        return ans

    def countCorrectAnswers(self, preguntasRespondidas):
        c = 0
        for pr in preguntasRespondidas:
            for r in pr:
                if r['RespuestaSeleccionada'] == r['RespuestaCorrecta']:
                    c += 1
        return c

    def get(self, request, id=0):
        #Muestra las preguntas
        preguntas = list(Pregunta.objects.values())
        if len(preguntas) > 0:
            datos = {'Message': "Success GET", 'Preguntas': preguntas}
        else:
            datos = {'Message': "Preguntas not found..."}
        return Response(datos)

    def post(self, request):
        #Captura los datos enviados por el frontend y envía un mensaje
        print(request.body)
        jd = json.loads(request.body)
        preguntas = list(Pregunta.objects.values())
        datos = {}
        if int(jd['IdPregunta']) >= 0:
            #Guardar las preguntas respondidas
            ans = self.isAnswered(jd['IdPregunta'], jd['IdExamenXUsuario'])
            if ans:
                self.updatePreguntasXExamenXUsuario(jd['IdPregunta'], jd['IdExamenXUsuario'], jd['Respuesta'], jd['RespuestaCorrecta'])
            else:
                self.createPreguntasXExamenXUsuario(jd['IdPregunta'], jd['IdUsuario'], jd['IdExamenXUsuario'], jd['Respuesta'], jd['RespuestaCorrecta'])
            datos = {'Message': 'Success POST', 'IdPregunta': jd['IdPregunta'], 'IdUsuario': jd['IdUsuario'], 'IdExamenXUsuario': jd['IdExamenXUsuario'], 'RespuestaSeleccionada': jd['Respuesta'], 'RespuestaCorrecta': jd['RespuestaCorrecta']}
        else:
            #Enviar las respuestas del usuario para el feedback
            usuario = Usuario.objects.filter(IdUsuario = int(jd['IdUsuario']))
            examenXUsuario = ExamenesXUsuario.objects.filter(IdExamenesXUsuario = int(jd['IdExamenXUsuario']))
            preguntasXExamenXUsuarios = PreguntasXExamenXUsuario.objects.filter(IdUsuario = usuario[0], IdExamenesXUsuario = examenXUsuario[0])
            preguntasRespondidas = []
            for peu in preguntasXExamenXUsuarios:
                pregunta = Pregunta.objects.filter(IdPregunta = peu.IdPregunta.IdPregunta)
                serializer = PreguntaSerializer(pregunta, many=True)
                newData = list(serializer.data)
                newData[0].update({'RespuestaSeleccionada': peu.RespuestaSeleccionada})
                preguntasRespondidas.append(newData)
            nCorrectas = self.countCorrectAnswers(preguntasRespondidas)
            nPreguntas = len(preguntasXExamenXUsuarios)
            examenXUsuario.update(PreguntasCorrectas = nCorrectas, TotalPreguntas = nPreguntas)
            datos = {'Message': 'Success POST', 'Preguntas': preguntasRespondidas, 'IdUsuario': jd['IdUsuario'], 'IdExamenXUsuario': jd['IdExamenXUsuario'], 'Correctas': nCorrectas, 'NroPreguntas': nPreguntas}
        return JsonResponse(datos)


