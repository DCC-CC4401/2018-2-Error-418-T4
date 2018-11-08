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

class EquipoTrabajo(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE())

    def __str__(self):
        return self.nombre

class IntegrantesEquipo(models.Model):
    id_equipo = models.ForeignKey(EquipoTrabajo, related_name='id_equipo', on_delete=models.CASCADE())
    nombre_equipo = models.ForeignKey(EquipoTrabajo, related_name='nombre', on_delete=models.CASCADE())
    rut_estudiante = models.ForeignKey(PersonaNatural, related_name='rut', on_delete=models.CASCADE())
    nombre_estudiante = models.ForeignKey(PersonaNatural, related_name='nombre', on_delete=models.CASCADE())

class HistorialEquipos(models.Model):
    id_equipo = models.ForeignKey(EquipoTrabajo, on_delete=models.CASCADE())
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE())
    rut_estudiante = models.ForeignKey(PersonaNatural, related_name='rut', on_delete=models.CASCADE())
    nombre_estudiante = models.ForeignKey(PersonaNatural, related_name='nombre', on_delete=models.CASCADE())

class Administrador(models.Model):
    rut_admin = models.CharField(max_length=12, primary_key=True)
    nombre_admin = models.CharField(max_length=35)
    apellido_admin = models.CharField(max_length=35)
    contraseña = forms.CharField(widget=forms.PasswordInput)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)