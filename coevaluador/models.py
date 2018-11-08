from django.db import models

# Create your models here.
from django.forms import forms


class Coevaluacion(models.Model):
    id_coev=models.CharField(max_length=50)
    n_preguntas= models.IntegerField()
    estado= models.CharField(max_length=50)
    f_inicio= models.DateField()
    f_termino=models.DateField()
    id_curso=models.ForeignKey(Curso, on_delete=models.CASCADE())



class FichaCoevaluacion(models.Model):
     id=models.CharField(max_length=50)
     id_equipo=models.ForeignKey(Equipos, on_delete=models.CASCADE())
     id_curso=models.ForeignKey(Curso, on_delete=models.CASCADE())
     id_coev=models.ForeignKey(Coevaluacion, on_delete=models.CASCADE())
     id_alumno= models.ForeignKey(PersonaNatural, on_delete=models.CASCADE())
     estado= models.ForeignKey(Coevaluacion, on_delete=models.CASCADE())
     nota= models.FloatField()

class Preguntas(models.Model):
    id_pregunta= models.CharField(max_length=50)
    pregunta= models.CharField(max_length=500)
    id_curso= models.ForeignKey(Curso, on_delete=models.CASCADE())

class Respuestas(models.Model):
    id_coevaluacion=models.ForeignKey(Coevaluacion, on_delete=models.CASCADE())
    id_evaluador= models.ForeignKey(PersonaNatural, on_delete=models.CASCADE())
    id_evaluado=models.ForeignKey(PersonaNatural, on_delete=models.CASCADE())
    id_pregunta= models.ForeignKey(Preguntas, on_delete=models.CASCADE())
    nota= models.FloatField()

class WorkTeams(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE())

    def __str__(self):
        return self.team_name

class TeamMembers(models.Model):
    team_id = models.ForeignKey(WorkTeams, related_name='team_id', on_delete=models.CASCADE())
    team_name = models.ForeignKey(WorkTeams, related_name='team_name', on_delete=models.CASCADE())
    student_rut = models.ForeignKey(NaturalPerson, related_name='rut', on_delete=models.CASCADE())
    student_name = models.ForeignKey(NaturalPerson, related_name='name', on_delete=models.CASCADE())

class TeamHistory(models.Model):
    team_id = models.ForeignKey(WorkTeams, on_delete=models.CASCADE())
    team_name = models.ForeignKey(WorkTeams, related_name='team_name', on_delete=models.CASCADE())
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE())
    student_rut = models.ForeignKey(NaturalPerson, related_name='rut', on_delete=models.CASCADE())
    student_name = models.ForeignKey(NaturalPerson, related_name='name', on_delete=models.CASCADE())

class Admin(models.Model):
    admin_rut = models.CharField(max_length=12, primary_key=True)
    admin_name = models.CharField(max_length=35)
    admin_surname = models.CharField(max_length=35)
    password = forms.CharField(widget=forms.PasswordInput)

    def __str__(self):
        return '%s %s' % (self.admin_name, self.admin_surname)