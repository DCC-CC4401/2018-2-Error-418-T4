from django.db import models

# Create your models here.
from django import forms


class NaturalPerson(models.Model):
    rut = models.CharField(max_length=50, primary_key=True)
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
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Coevaluation(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    n_questions = models.IntegerField()
    status = models.CharField(max_length=50)
    s_date = models.DateField()
    e_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


# Segun yo esto no tiene mucho sentido, pero por mientras lo dejaremos así para ver como sale
class CourseRecordForStudent(models.Model):
    student = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rol = models.CharField(max_length=100)
    coevaluation = models.ForeignKey(Coevaluation, on_delete=models.CASCADE)


class Team(models.Model):
    pass


class CoevaluationSheet(models.Model):
    id = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    coevaluation = models.ForeignKey(Coevaluation, on_delete=models.CASCADE)
    student = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    grade = models.FloatField()


class Question(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    question = models.CharField(max_length=500)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Answer(models.Model):
    coevaluation = models.ForeignKey(Coevaluation, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE)
    evaluated = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    grade = models.FloatField()
