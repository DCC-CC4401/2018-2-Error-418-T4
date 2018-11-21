from django.contrib import messages
from django.contrib.auth import authenticate, login as lgi, logout as lgo
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginForm
from .models import *

# Use underscore separated words for views like hello_world.

SEMESTER = ['Verano', 'Otoño', 'Primavera']


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
            user = authenticate(request, rut=rut, password=password)
            if user is not None:
                lgi(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('coevaluador:home'))
            else:
                # Return an 'invalid login' error message.
                messages.error(request, "El rut o la contraseña son incorrectas")
                return HttpResponseRedirect(reverse('coevaluador:login'))

    # if a GET (or any other method) we'll create a blank form
    else:
        if request.user.is_authenticated:
            return home(request)
        form = LoginForm()

    return render(request, 'coevaluador/login.html', {'form': form})


def logout(request):
    lgo(request)
    return render(request, 'coevaluador/logout.html')


def home(request):
    if request.user.is_authenticated:
        user = request.user
        st = user.courses_as_student.all()
        au = user.courses_as_auxiliary.all()
        ai = user.courses_as_aide.all()
        te = user.courses_as_teacher.all()
        courses = st.union(au, ai, te)
        cst = Coevaluation.objects.filter(course__in=st)
        c_sheets = CoevaluationSheet.objects.filter(coevaluation__in=cst, student=user)
        cau = Coevaluation.objects.filter(course__in=au)
        cai = Coevaluation.objects.filter(course__in=ai)
        cte = Coevaluation.objects.filter(course__in=te)
        coevaluations = cst.union(cau, cai, cte)
        context = {
            'c_sheets': c_sheets.all(),
            'coevaluations': coevaluations.order_by('e_date').reverse(),
            'courses': courses.order_by('name'),
            'courses_as_student': user.courses_as_student.all(),
            'courses_as_auxiliary': user.courses_as_auxiliary.all(),
            'courses_as_aide': user.courses_as_aide.all(),
            'courses_as_teacher': user.courses_as_teacher.all(),
        }
        return render(request, 'coevaluador/home.html', context)
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


def add_co_evaluation(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            co_title = request.POST['co_title']
            course_year = request.POST['course_year']
            course_semester = request.POST['course_semester']
            course_name = request.POST['course_name']
            course_section = request.POST['course_section']
            course_obj = Course.objects.get(year=course_year, semester=course_semester, name=course_name,
                                            section=course_section)
            s_date = request.POST['co_s_date']
            e_date = request.POST['co_e_date']
            co_evaluation = Coevaluation(name=co_title, status="Abierta", s_date=s_date, e_date=e_date,
                                         course=course_obj)
            co_evaluation.save()
            return HttpResponseRedirect(reverse('coevaluador:course',
                                                args=(course_obj.year, course_obj.semester, course_obj.code,
                                                      course_obj.section)))


def course(request, year, semester, code, section):
    user = request.user
    if user.is_authenticated:
        try:

            course_obj = Course.objects.get(year=year, semester=semester, code=code, section=section)

            context = {
                'course': course_obj,
                'sem_str': SEMESTER[semester]
            }

            if course_obj in user.courses_as_student.all():
                co_ev = Coevaluation.objects.filter(course=course_obj)
                c_sheets = CoevaluationSheet.objects.filter(coevaluation__in=co_ev, student=user)
                context['coevaluations'] = co_ev.order_by('e_date').reverse()
                context['c_sheets'] = c_sheets.all()
                return render(request, 'coevaluador/studentCourse.html', context)
            else:
                coevaluations = Coevaluation.objects.filter(course=course_obj)
                published_coevaluations = coevaluations.filter(status='Publicada')
                context['coevaluations'] = coevaluations.order_by('e_date').reverse()
                context['published_co_evs'] = published_coevaluations.order_by('s_date')
                work_teams = course_obj.workteam_set.all()
                wts = []
                for wt in work_teams:
                    members = wt.teammember_set.all()
                    wt_mem = []
                    for m in members:
                        wt_mem.append(m)
                    wt_arr = [wt, wt_mem]
                    wts.append(wt_arr)
                context['work_teams'] = wts
                return render(request, 'coevaluador/teachingCourse.html', context)

        except Course.DoesNotExist:
            HttpResponseRedirect(reverse('coevaluador:login'))
    return HttpResponseRedirect(reverse('coevaluador:login'))


def student_course(request):
    return render(request, 'coevaluador/studentCourse.html')


def teaching_course(request):
    return render(request, 'coevaluador/teachingCourse.html')


def owner_profile(request):
    return render(request, 'coevaluador/ownerProfile.html')


def teaching_profile(request):
    return render(request, 'coevaluador/teachingProfile.html')
