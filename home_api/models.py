from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class Examen(models.Model):
	IdExamen = models.PositiveSmallIntegerField(default=5, primary_key=True)
	Nombre = models.CharField(max_length=50)
	Precio = models.IntegerField()
	Duracion = models.DurationField()
	NroPreguntas = models.IntegerField()

	def __str__(self):
		txt = 'Examen {1} N°{0}'
		return txt.format(self.IdExamen, self.Nombre)

class Especialidad(models.Model):
	IdEspecialidad = models.PositiveSmallIntegerField(default=5, primary_key=True)
	Nombre = models.CharField(max_length=50)

	def __str__(self):
		txt = "{0}"
		return txt.format(self.Nombre)

	def save(self, *args, **kwargs):
		examenes = list(Examen.objects.values())
		idExamen = len(examenes)+1
		Examen.objects.create(IdExamen = idExamen, Nombre = self.Nombre, Precio = 50000, Duracion = '02:00:00', NroPreguntas = 40)
		super(Especialidad, self).save(*args, **kwargs)

class Usuario(models.Model):
	IdUsuario = models.IntegerField(primary_key=True)
	Nombre = models.CharField(null=True, max_length=35)
	ApellidoPaterno = models.CharField(null=True, max_length=35)
	Edad = models.IntegerField(null=True)
	sexos = [
		('O', 'Otro'),
		('F', 'Femenino'),
		('M', 'Masculino')
	]
	Sexo = models.CharField(max_length=15, choices=sexos, default='O')
	FechaNacimiento = models.DateField(null=True)
	Usuario = models.CharField(unique=True, max_length=50) 
	Email = models.EmailField(unique=True)
	Contrasena = models.CharField(max_length=50)
	
	def __str__(self):
		txt = '{0} {1}'
		return txt.format(self.Nombre, self.ApellidoPaterno)

class Pregunta(models.Model):
	IdPregunta = models.IntegerField(primary_key=True)
	Pregunta = models.CharField(max_length=1500)
	OpcionA = models.CharField(max_length=500)
	OpcionB = models.CharField(max_length=500)
	OpcionC = models.CharField(max_length=500)
	OpcionD = models.CharField(max_length=500)
	respuestas = [('A', 'OpcionA'), ('B', 'OpcionB'), ('C', 'OpcionC'), ('D', 'OpcionD')]
	RespuestaCorrecta = models.CharField(max_length=10, choices = respuestas)
	Explicacion = models.CharField(max_length=3000)
	IdEspecialidad = models.ForeignKey(Especialidad, null=False, blank=False, on_delete=models.CASCADE)

	def __str__(self):
		txt = 'Pregunta N°{0}'
		return txt.format(self.IdPregunta)

class ExamenesXUsuario(models.Model):
	IdExamenesXUsuario = models.IntegerField(primary_key=True)
	IdExamen = models.ForeignKey(Examen, null=False, blank=False, on_delete=models.CASCADE)
	IdUsuario = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE)
	PreguntasCorrectas = models.IntegerField(null=True)
	TotalPreguntas = models.IntegerField(null=True)

	def __str__(self):
		txt = '{1} de {2} N°{0}'
		return txt.format(self.IdExamenesXUsuario, self.IdExamen, self.IdUsuario)

class PreguntasXExamenes(models.Model):
	IdPreguntasXExamenes = models.IntegerField(primary_key=True)
	IdPregunta = models.ForeignKey(Pregunta, null=False, blank=False, on_delete=models.CASCADE)
	IdExamen = models.ForeignKey(Examen, null=False, blank=False, on_delete=models.CASCADE)

class ExamenesXEspecialidad(models.Model):
	IdExamenesXEspecialidad = models.IntegerField(primary_key=True)
	IdEspecialidad = models.ForeignKey(Especialidad, null=False, blank=False, on_delete=models.CASCADE)
	IdExamen = models.ForeignKey(Examen, null=False, blank=False, on_delete=models.CASCADE)

class PreguntasXExamenXUsuario(models.Model):
	IdPreguntasXExamenXUsuario = models.IntegerField(primary_key=True)
	IdPregunta = models.ForeignKey(Pregunta, null=False, blank=False, on_delete=models.CASCADE)
	IdExamenesXUsuario = models.ForeignKey(ExamenesXUsuario, null=False, blank=False, on_delete=models.CASCADE)
	IdUsuario = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE)
	RespuestaSeleccionada = models.CharField(max_length=2, null=True)
	Correcta = models.BooleanField(null=False)

	def __str__(self):
		txt = '{1}, {2} N°{0}'
		return txt.format(self.IdPreguntasXExamenXUsuario, self.IdExamenesXUsuario, self.IdPregunta)



