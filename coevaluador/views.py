from django.shortcuts import render


def index(request):
    return render(request, 'coevaluador/index.html')


def admi(request):
    return render(request, 'coevaluador/admi.html')


def LandingPagePersonaNat(request):
    return render(request, 'coevaluador/LandingPagePersonaNat.html')


def LandingPageEqD(request):
    return render(request, 'coevaluador/LandingPageEqD.html')


def course(request):
    return render(request, 'coevaluador/course.html')

def courseStudent(request):
    return render(request, 'coevaluador/courseStudent.html')

def profile(request):
    return render(request, 'coevaluador/profile.html')


def StudentProfile(request):
    return render(request, 'coevaluador/StudentProfile.html')


def adminStudentProfile(request):
    return render(request, 'coevaluador/adminStudentProfile.html')


def coevaluation(request):
    return render(request, 'coevaluador/coev.html')
