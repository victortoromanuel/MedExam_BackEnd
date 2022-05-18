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
class FormularioView(APIView):


    def setIdExamenXUsuario(self):
        maxi = 0
        examenes = list(ExamenesXUsuario.objects.values())
        for e in examenes:
            if e['IdExamenesXUsuario'] > maxi:
                maxi = e['IdExamenesXUsuario']
        return maxi+1

    def setIdPreguntas(self):
        maxi = 0
        pregunta = list(PreguntasXExamenXUsuario.objects.values())
        for p in pregunta:
            if p['IdPreguntasXExamenXUsuario'] > maxi:
                maxi = p['IdPreguntasXExamenXUsuario']
        return maxi+1

    def createExamenXUsuario(self, idUsuario, idExamen):
        #idExamen = 0 (Gratis), 1 (Corto), 2 (Largo)
        examenes = list(ExamenesXUsuario.objects.values())
        idExamenXUsuario = self.setIdExamenXUsuario()
        examenGratis = Examen.objects.filter(IdExamen = idExamen)
        usuario = Usuario.objects.filter(IdUsuario = idUsuario)
        ExamenesXUsuario.objects.create(IdExamenesXUsuario = idExamenXUsuario, IdExamen = examenGratis[0], IdUsuario = usuario[0])
        return idExamenXUsuario

    def createPreguntasXExamenXUsuario(self, pregunta, idUsuario, idExamenXUsuario, respuestaSeleccionada, respuestaCorrecta):
        #Crea la instancia de la pregunta respondida por el usuario en ese examen y verifica si correctitud
        preguntasXExamenXUsuarios = list(PreguntasXExamenXUsuario.objects.values())
        idPreguntasXExamenXUsuario = self.setIdPreguntas()
        usuario = Usuario.objects.filter(IdUsuario = int(idUsuario))
        examenXUsuario = ExamenesXUsuario.objects.filter(IdExamenesXUsuario = int(idExamenXUsuario))
        correcta = False
        if respuestaSeleccionada == respuestaCorrecta:
            correcta = True
        PreguntasXExamenXUsuario.objects.create(IdPreguntasXExamenXUsuario = idPreguntasXExamenXUsuario, IdPregunta = pregunta, IdUsuario = usuario[0], IdExamenesXUsuario = examenXUsuario[0], RespuestaSeleccionada = respuestaSeleccionada, Correcta = correcta)
        return
    
    def examExist(self, idExamenXUsuario):
        #Retorna True si el ExamenXUsuario ya existe y False en caso de no existir.
        ans = False
        examenXUsuario = ExamenesXUsuario.objects.filter(IdExamenesXUsuario = int(idExamenXUsuario))
        preguntasXExamenXUsuarios = PreguntasXExamenXUsuario.objects.filter(IdExamenesXUsuario = examenXUsuario[0])
        if len(preguntasXExamenXUsuarios) > 0:
            ans = True
        print(ans)
        return ans

    def generatePreguntas(self, nroTotalPreguntas, maxPreguntasExamen, idUsuario, idExamenXUsuario):
        preguntasElegidas = []
        idPreguntas = random.sample(range(1, nroTotalPreguntas), maxPreguntasExamen)
        for i in idPreguntas:
            pregunta = Pregunta.objects.filter(IdPregunta = i)
            self.createPreguntasXExamenXUsuario(pregunta[0], idUsuario, idExamenXUsuario, 'N', pregunta[0].RespuestaCorrecta)
            serializer = PreguntaSerializer(pregunta, many=True)
            preguntasElegidas.append(serializer.data)
        return preguntasElegidas

    def generatePreguntasEspecialidad(self, nroTotalPreguntas, maxPreguntasExamen, idUsuario, idExamenXUsuario, idEspecialidad):
        preguntasElegidas = []
        #idPreguntas = random.sample(range(1, nroTotalPreguntas), maxPreguntasExamen)
        especialidad = Especialidad.objects.filter(IdEspecialidad = idEspecialidad)
        preguntas = list(Pregunta.objects.filter(IdEspecialidad = especialidad[0]))
        random.shuffle(preguntas)
        for i in range(maxPreguntasExamen):
            pregunta = Pregunta.objects.filter(IdPregunta = preguntas[i].IdPregunta, IdEspecialidad = especialidad[0])
            self.createPreguntasXExamenXUsuario(pregunta[0], idUsuario, idExamenXUsuario, 'N', pregunta[0].RespuestaCorrecta)
            serializer = PreguntaSerializer(pregunta, many=True)
            preguntasElegidas.append(serializer.data)
        return preguntasElegidas

    def getPreguntasXExamenXUsuario(self, idUsuario, idExamenXUsuario):
        usuario = Usuario.objects.filter(IdUsuario = int(idUsuario))
        examenXUsuario = ExamenesXUsuario.objects.filter(IdExamenesXUsuario = int(idExamenXUsuario))
        preguntasXExamenXUsuarios = PreguntasXExamenXUsuario.objects.filter(IdExamenesXUsuario = examenXUsuario[0], IdUsuario = usuario[0])
        preguntasElegidas = []
        for peu in preguntasXExamenXUsuarios:
            pregunta = Pregunta.objects.filter(IdPregunta = peu.IdPregunta.IdPregunta)
            print(peu.IdPregunta.IdPregunta)
            serializer = PreguntaSerializer(pregunta, many=True)
            preguntasElegidas.append(serializer.data)
        return preguntasElegidas

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
        if jd['Nombre'] == "Examen gratis":
            if jd['getPregunta'] == False: #Envía el idExamenXUsuario
                idExamenXUsuario = self.createExamenXUsuario(int(jd['IdUsuario']), 0)
                datos = {'Message': 'Success POST', 'IdExamenXUsuario': idExamenXUsuario}
            else: #Se crea el ExamenXUsuario
                preguntasElegidas = []
                if self.examExist(jd['IdExamenXUsuario']): #Si ya existe el examen con preguntas, se envían las preguntas
                    preguntasElegidas = self.getPreguntasXExamenXUsuario(jd['IdUsuario'], jd['IdExamenXUsuario'])
                else: #Sino se crean las preguntas
                    preguntasElegidas = self.generatePreguntas(len(preguntas), 5, jd['IdUsuario'], jd['IdExamenXUsuario'])
                nombreExamen = Examen.objects.filter(IdExamen = 0)
                datos = {'Message': 'Success POST', 'Preguntas': preguntasElegidas, 'NombreExamen': nombreExamen[0].Nombre, 'IdExamen': 0, 'IdExamenXUsuario': jd['IdExamenXUsuario'], 'Tiempo': 15}

        elif jd['Nombre'] == "Examen corto":
            if jd['getPregunta'] == False: #Envía el idExamenXUsuario
                idExamenXUsuario = self.createExamenXUsuario(int(jd['IdUsuario']), 1)
                datos = {'Message': 'Success POST', 'IdExamenXUsuario': idExamenXUsuario}
            else: #Se crea el ExamenXUsuario
                preguntasElegidas = []
                if self.examExist(jd['IdExamenXUsuario']): #Si ya existe el examen con preguntas, se envían las preguntas
                    preguntasElegidas = self.getPreguntasXExamenXUsuario(jd['IdUsuario'], jd['IdExamenXUsuario'])
                else: #Sino se crean las preguntas
                    preguntasElegidas = self.generatePreguntas(len(preguntas), 20, jd['IdUsuario'], jd['IdExamenXUsuario']) #Cambiar el 20 por 30 en producción
                nombreExamen = Examen.objects.filter(IdExamen = 1)
                datos = {'Message': 'Success POST', 'Preguntas': preguntasElegidas, 'NombreExamen': nombreExamen[0].Nombre, 'IdExamen': 1, 'IdExamenXUsuario': jd['IdExamenXUsuario'], 'Tiempo': 90}

        elif jd['Nombre'] == "Examen largo":
            if jd['getPregunta'] == False: #Envía el idExamenXUsuario
                idExamenXUsuario = self.createExamenXUsuario(int(jd['IdUsuario']), 2)
                datos = {'Message': 'Success POST', 'IdExamenXUsuario': idExamenXUsuario}
            else: #Se crea el ExamenXUsuario
                preguntasElegidas = []
                if self.examExist(jd['IdExamenXUsuario']): #Si ya existe el examen con preguntas, se envían las preguntas
                    preguntasElegidas = self.getPreguntasXExamenXUsuario(jd['IdUsuario'], jd['IdExamenXUsuario'])
                else: #Sino se crean las preguntas
                    preguntasElegidas = self.generatePreguntas(len(preguntas), 20, jd['IdUsuario'], jd['IdExamenXUsuario']) #Cambiar el 20 por 50 en producción
                nombreExamen = Examen.objects.filter(IdExamen = 2)
                datos = {'Message': 'Success POST', 'Preguntas': preguntasElegidas, 'NombreExamen': nombreExamen[0].Nombre, 'IdExamen': 2, 'IdExamenXUsuario': jd['IdExamenXUsuario'], 'Tiempo': 150}

        elif jd['Nombre'] == "Examen especializado":
            if jd['getPregunta'] == False: #Envía el idExamenXUsuario
                idExamenXUsuario = self.createExamenXUsuario(int(jd['IdUsuario']), int(jd['IdEspecialidad'])+2)
                datos = {'Message': 'Success POST', 'IdExamenXUsuario': idExamenXUsuario}
            else: #Se crea el ExamenXUsuario
                nombreExamen = Especialidad.objects.filter(IdEspecialidad = int(jd['IdEspecialidad'])-2)
                preguntasElegidas = []
                if self.examExist(jd['IdExamenXUsuario']): #Si ya existe el examen con preguntas, se envían las preguntas
                    preguntasElegidas = self.getPreguntasXExamenXUsuario(jd['IdUsuario'], jd['IdExamenXUsuario'])
                else: #Sino se crean las preguntas
                    preguntasElegidas = self.generatePreguntasEspecialidad(len(preguntas), 10, jd['IdUsuario'], jd['IdExamenXUsuario'], int(jd['IdEspecialidad'])-2) #Cambiar el 20 por 40 en producción
                datos = {'Message': 'Success POST', 'Preguntas': preguntasElegidas, 'NombreExamen': nombreExamen[0].Nombre,'IdExamen': int(jd['IdEspecialidad']), 'IdExamenXUsuario': jd['IdExamenXUsuario'], 'Tiempo': 120}
        return JsonResponse(datos)

