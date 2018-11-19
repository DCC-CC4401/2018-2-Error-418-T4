from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from coevaluador.models import Coevaluation, CoevaluationSheet
from .models import Course
from .forms import LoginForm
from .models import User

# Use underscore separated words for views like hello_world.


def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            rut = form.cleaned_data['rut']
            password = form.cleaned_data['password']
            # redirect to a new URL:
            try:
                user = User.objects.get(rut=rut, password=password)
                if user.is_teacher or user.is_auxiliary or user.is_aide:
                    return HttpResponseRedirect(reverse('coevaluador:teachingHome'))
                if user.is_student:
                    return HttpResponseRedirect(reverse('coevaluador:studentHome', args=rut))
                if user.is_admin:
                    return HttpResponseRedirect(reverse('coevaluador:admin'))
            except User.DoesNotExist:
                context = {'error': 'El usuario no existe'}
                return render(request, 'coevaluador/login.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'coevaluador/login.html', {'form': form})


def student_home(request, rut):
    student_courses = User.objects.get(rut=rut).courses_as_student.order_by("year", "semester")
    student_coev_sheets = CoevaluationSheet.objects.filter(student=rut)
    student_coev = list()
    for obj in student_coev_sheets:
        student_coev.append(obj.coevaluation)
    student_coev.sort(key=lambda coev:coev.status)
    return render(request, 'coevaluador/studentHome.html', {
        "student_courses":student_courses,
        "student_coevaluations":student_coev,
        "student_coevaluation_sheets":student_coev_sheets
    })


def teaching_home(request):
    return render(request, 'coevaluador/teachingHome.html')


def student_coevaluation(request):
    return render(request, 'coevaluador/studentCoevaluation.html')


def teaching_coevaluation(request):
    return render(request, 'coevaluador/teachingCoevaluation.html')


def student_course(request):
    return render(request, 'coevaluador/studentCourse.html')


def teaching_course(request):
    return render(request, 'coevaluador/teachingCourse.html')


def owner_profile(request):
    return render(request, 'coevaluador/ownerProfile.html')


def teaching_profile(request):
    return render(request, 'coevaluador/teachingProfile.html')
