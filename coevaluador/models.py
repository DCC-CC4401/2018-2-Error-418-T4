from django.db import models

# Create your models here.
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