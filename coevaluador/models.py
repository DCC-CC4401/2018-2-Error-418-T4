from django.db import models
from django.utils import timezone


class User(models.Model):
    rut = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Question(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    question = models.CharField(max_length=500)


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=30)
    year = models.IntegerField()
    semester = models.IntegerField()
    students = models.ManyToManyField(User, related_name='courses_as_student')
    auxiliaries = models.ManyToManyField(User, related_name='courses_as_auxiliary')
    aides = models.ManyToManyField(User, related_name='courses_as_aide')
    teachers = models.ManyToManyField(User, related_name='courses_as_teacher')
    questions = models.ManyToManyField(Question, blank=True)


class WorkTeam(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    work_team = models.ForeignKey(WorkTeam, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class TeamRecordForStudent(models.Model):
    work_teams = models.ForeignKey(WorkTeam, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class Coevaluation(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    status = models.CharField(max_length=50)
    s_date = models.DateField()
    e_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.ManyToManyField(Question, on_delete=models.CASCADE)


# Segun yo esto no tiene mucho sentido, pero por mientras lo dejaremos así para ver como sale
class CourseRecordForStudent(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rol = models.CharField(max_length=100)
    coevaluation = models.ForeignKey(Coevaluation, on_delete=models.CASCADE)


class Answer(models.Model):
    coevaluation = models.ForeignKey(Coevaluation, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(User, related_name='evaluator', on_delete=models.CASCADE)
    evaluated = models.ForeignKey(User, related_name='evaluated', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)


class CoevaluationSheet(models.Model):
    team = models.ForeignKey(WorkTeam, on_delete=models.CASCADE)
    coevaluation = models.ForeignKey(Coevaluation, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Many To Many????
    status = models.CharField(max_length=100)
    answers = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True)


class Admin(models.Model):
    rut = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
