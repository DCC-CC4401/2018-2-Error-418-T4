from django.db import models


class NaturalPerson(models.Model):
    rut = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)


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
    password = models.CharField(max_length=50)
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


class WorkTeam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    work_team = models.ForeignKey(WorkTeam, on_delete=models.CASCADE)
    student = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE)


class TeamRecordForStudent(models.Model):
    work_team = models.ForeignKey(WorkTeam, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(NaturalPerson, on_delete=models.CASCADE)


class CoevaluationSheet(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    team = models.ForeignKey(WorkTeam, on_delete=models.CASCADE)
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
    evaluator = models.ForeignKey(NaturalPerson, related_name='evaluator', on_delete=models.CASCADE)
    evaluated = models.ForeignKey(NaturalPerson, related_name='evaluated', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    grade = models.FloatField()


class Admin(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=35)
    surname = models.CharField(max_length=35)
    password = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s' % (self.name, self.surname)
