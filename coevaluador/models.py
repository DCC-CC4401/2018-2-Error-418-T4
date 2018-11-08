from django.db import models

# Create your models here.
from django import forms


class NaturalPerson(models.Model):
    rut = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(widget=forms.PasswordInput)


class Course(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=30)
    year = models.IntegerField()
    semester = models.IntegerField()


class TeachingTeamMember(models.Model):
    rut = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(widget=forms.PasswordInput)
    rol = models.CharField(max_length=100)
    course = models.ForeignKey(Course)


class Coevaluation(models.Model):
    id_coev = models.CharField(max_length=50)
    n_preguntas = models.IntegerField()
    estado = models.CharField(max_length=50)
    f_inicio = models.DateField()
    f_termino = models.DateField()
    id_curso = models.ForeignKey(Course, on_delete=models.CASCADE())


# Segun yo esto no tiene mucho sentido, pero por mientras lo dejaremos así para ver como sale
class CourseRecordForStudent(models.Model):
    student = models.ForeignKey(NaturalPerson)
    course = models.ForeignKey(Course)
    rol = models.CharField(max_length=100)
    coevaluation = models.ForeignKey(Coevaluation)


class Team(models.Model):
    pass


class FichaCoevaluacion(models.Model):
    id = models.CharField(max_length=50)
    id_equipo = models.ForeignKey(Team, on_delete=models.CASCADE())
    id_curso = models.ForeignKey(Course, on_delete=models.CASCADE())
    id_coev = models.ForeignKey(Coevaluation, on_delete=models.CASCADE())
    id_alumno = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE())
    estado = models.ForeignKey(Coevaluation, on_delete=models.CASCADE())
    nota = models.FloatField()


class Preguntas(models.Model):
    id_pregunta = models.CharField(max_length=50)
    pregunta = models.CharField(max_length=500)
    id_curso = models.ForeignKey(Course, on_delete=models.CASCADE())


class Respuestas(models.Model):
    id_coevaluacion = models.ForeignKey(Coevaluation, on_delete=models.CASCADE())
    id_evaluador = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE())
    id_evaluado = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE())
    id_pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE())
    nota = models.FloatField()
