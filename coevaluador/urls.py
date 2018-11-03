from django.urls import path

from . import views

app_name = 'coevaluador'

urlpatterns = [
    path('', views.index, name='index'),
    path('admi', views.admi, name='admi'),
    path('LPPN', views.LandingPagePersonaNat, name='LandingPagePersonaNat'),
    path('LPED', views.LandingPageEqD, name='LandingPageEqD'),
    path('course', views.course, name='course'),
    path('profile', views.profile, name='profile'),
    path('student', views.StudentProfile, name='StudentProfile'),
    path('adstudent', views.adminStudentProfile, name='adminStudentProfile'),
    path('coev', views.coevaluation, name='coev'),
    path('courseStudent', views.courseStudent, name='courseStudent'),
]
