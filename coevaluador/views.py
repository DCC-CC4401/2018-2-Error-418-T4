from django.contrib import messages
from django.contrib.auth import authenticate, login as lgi, logout as lgo
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginForm
from .utils import escape_rut


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
            rut = escape_rut(rut)
            password = form.cleaned_data['password']
            print(rut, password)
            user = authenticate(request, rut=rut, password=password)
            if user is not None:
                lgi(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('coevaluador:home'))
            else:
                print(user)
                # Return an 'invalid login' error message.
                messages.error(request, "El rut o la contraseña son incorrectas")
                return HttpResponseRedirect(reverse('coevaluador:login'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'coevaluador/login.html', {'form': form})


def logout(request):
    lgo(request)
    return render(request, 'coevaluador/logout.html')


def home(request):
    if request.user.is_authenticated:
        return render(request, 'coevaluador/home.html')
    else:
        form = LoginForm()
        return render(request, 'coevaluador/login.html', {'form': form})


def student_home(request):
    return render(request, 'coevaluador/studentHome.html')


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
