from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from home_api.models import *

# Register your models here.
admin.site.register(Especialidad)
admin.site.register(Usuario)
admin.site.register(Examen)
admin.site.register(ExamenesXUsuario)
admin.site.register(PreguntasXExamenes)
admin.site.register(ExamenesXEspecialidad)
admin.site.register(PreguntasXExamenXUsuario)

#Import export
class PreguntaResources(resources.ModelResource):
    class Meta:
        model = Pregunta
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['IdPregunta']
        exclude = ('id',)
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

@admin.register(Pregunta)
class PreguntaAdmin(ImportExportModelAdmin):
    resource_class = PreguntaResources
