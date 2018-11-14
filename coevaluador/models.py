from django.db import models
from django.utils import timezone


class User(models.Model):
    rut = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    date_joined = models.DateTimeField(default=timezone.now)

    is_student = models.BooleanField('student status', default=False)
    is_auxiliary = models.BooleanField('auxiliary status', default=False)
    is_aide = models.BooleanField('teacher status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)
    is_admin = models.BooleanField('admin status', default=False)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Course(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=30)
    year = models.IntegerField()
    semester = models.IntegerField()
    students = models.ManyToManyField(User)
    teaching_team_members = models.ManyToManyField(User)


class Coevaluation(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    n_questions = models.IntegerField()
    status = models.CharField(max_length=50)
    s_date = models.DateField()
    e_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


# Segun yo esto no tiene mucho sentido, pero por mientras lo dejaremos así para ver como sale
class CourseRecordForStudent(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rol = models.CharField(max_length=100)
    coevaluation = models.ForeignKey(Coevaluation, on_delete=models.CASCADE)


class WorkTeam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    work_team = models.ForeignKey(WorkTeam, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class TeamRecordForStudent(models.Model):
    work_team = models.ForeignKey(WorkTeam, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class CoevaluationSheet(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    team = models.ForeignKey(WorkTeam, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    coevaluation = models.ForeignKey(Coevaluation, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    grade = models.FloatField()


class Question(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    question = models.CharField(max_length=500)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Answer(models.Model):
    coevaluation = models.ForeignKey(Coevaluation, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(User, related_name='evaluator', on_delete=models.CASCADE)
    evaluated = models.ForeignKey(User, related_name='evaluated', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    grade = models.FloatField()


class Admin(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=35)
    surname = models.CharField(max_length=35)
    password = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' % (self.name, self.surname)
