from rest_framework.serializers import ModelSerializer
from home_api.models import Usuario

class UsuarioSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('Email', 'Usuario', 'Contrasena')