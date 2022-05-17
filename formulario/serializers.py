from rest_framework.serializers import ModelSerializer
from home_api.models import Pregunta

class PreguntaSerializer(ModelSerializer):
    class Meta:
        model = Pregunta
        fields = (
        'IdPregunta',
        'Pregunta',
        'OpcionA',
        'OpcionB',
        'OpcionC',
        'OpcionD',
        'RespuestaCorrecta',
        'Explicacion',
        'IdEspecialidad',
        )