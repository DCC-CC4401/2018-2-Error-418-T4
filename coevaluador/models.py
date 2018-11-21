from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from coevaluador.utils import escape_rut, RutValidator, validate


class UserManager(BaseUserManager):
    use_in_migrations = True

    rut_validator = RutValidator()

    def _create_user(self, rut, first_name, last_name, email, password, **extra_fields):
        """
        Create and save a user with the given rut, email, and password.
        """
        if not rut:
            raise ValueError('The given rut must be set')
        email = self.normalize_email(email)
        rut = self.model.normalize_username(rut)
        if validate(rut) is False:
            raise ValueError('The given rut is not valid')
        rut = escape_rut(rut)
        try:
            self.get(rut=rut)
            raise KeyError('User is already registered')

        except User.DoesNotExist:
            user = self.model(rut=rut, first_name=first_name, last_name=last_name, email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_user(self, rut, first_name, last_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(rut, first_name, last_name, email, password, **extra_fields)

    def create_superuser(self, rut, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(rut, first_name, last_name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    rut_validator = RutValidator()

    rut = models.CharField(
        _('rut'),
        max_length=50,
        unique=True,
        primary_key=True,
        help_text=_('El RUT puede contener caracteres "." y "-" pero no son necesarios.'),
        validators=[rut_validator],
        error_messages={
            'unique': _("Ya existe un usuario con ese RUT."),
        },
    )

    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    USERNAME_FIELD = 'rut'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_rut(self):
        return self.get_username()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return '%s - %s %s' % (self.rut, self.first_name, self.last_name)


class Question(models.Model):
    question = models.CharField(max_length=500)
    type_choices = (('rango', 'Rango'),
                    ('textbox', 'Cuadro de Texto'),
                    )

    type = models.CharField(max_length=100, choices=type_choices, default='rango')

    def __str__(self):
        return self.question


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=30)
    section = models.IntegerField()
    year = models.IntegerField()
    semester = models.IntegerField()
    students = models.ManyToManyField(User, related_name='courses_as_student')
    auxiliaries = models.ManyToManyField(User, related_name='courses_as_auxiliary', blank=True)
    aides = models.ManyToManyField(User, related_name='courses_as_aide', blank=True)
    teachers = models.ManyToManyField(User, related_name='courses_as_teacher')
    questions = models.ManyToManyField(Question, blank=True)

    def __str__(self):
        return '%s-%d %s' % (self.code, self.section, self.name)


class WorkTeam(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return '%s | %s' % (self.name, self.course)


class TeamMember(models.Model):
    work_team = models.ForeignKey(WorkTeam, related_name='wt_members', on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s / %s' % (self.student, self.work_team)


class TeamRecordForStudent(models.Model):
    work_teams = models.ForeignKey(WorkTeam, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class Coevaluation(models.Model):
    status_choices= (('Abierta', 'Abierta'), ('Cerrada','Cerrada'), ('Publicada', 'Publicada'))
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=status_choices, default='Abierta')
    s_date = models.DateTimeField()
    e_date = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.ManyToManyField(Question, blank=True)

    def __str__(self):
        return '%s / %s' % (self.name, self.course)


# Segun yo esto no tiene mucho sentido, pero por mientras lo dejaremos así para ver como sale
class CourseRecordForStudent(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rol = models.CharField(max_length=100)
    coevaluation = models.ForeignKey(Coevaluation, on_delete=models.CASCADE)


class CoevaluationSheet(models.Model):
    team = models.ForeignKey(WorkTeam, on_delete=models.CASCADE)
    coevaluation = models.ForeignKey(Coevaluation, on_delete=models.CASCADE)
    coevaluator = models.ForeignKey(User,related_name='coevaluator', on_delete=models.CASCADE)
    coevaluated= models.ForeignKey(User, related_name='coevaluated', on_delete=models.CASCADE)
    status_choices= (('answered','Contestada'), ('not_answered', 'Pendiente'))
    status = models.CharField(max_length=100, choices=status_choices, default='not_answered')
    grade= models.CharField(max_length=10, blank=True)

    def __str__(self):
        return '%s / %s / %s / %s' % (self.coevaluation, self.coevaluator, self.coevaluated,  self.status)

# class Response(models.Model):
#     evaluator= models.ForeignKey(User, )
#     evaluated= models.ForeignKey(User)

class Answer(models.Model):
    coevaluation_sheet = models.ForeignKey(CoevaluationSheet, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ans = models.CharField(max_length=1000)



class Admin(models.Model):
    rut = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
