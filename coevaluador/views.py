from django.contrib import messages
from django.contrib.auth import authenticate, login as lgi, logout as lgo
from django.contrib.auth.decorators import login_required
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
        c_sheets = CoevaluationSheet.objects.filter(coevaluation__in=cst, coevaluator=user)
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


@login_required(login_url='/login')
def coevaluation(request, coev_id, st_id=-1):
    user = request.user
    st_id = user.pk if st_id == -1 else st_id
    coevaluationsheet = CoevaluationSheet.objects.filter(coevaluation_id=coev_id, coevaluator=user,
                                                         coevaluated_id=st_id).first()
    coevaluation = Coevaluation.objects.get(id=coev_id)
    questions = coevaluation.question.all()

    if request.method == 'POST':
        for q in questions:
            ans = request.POST[str(q.id)]
            answer = Answer(coevaluation_sheet=coevaluationsheet, question=q, ans=ans)
            answer.save()
        coevaluationsheet.status = 'answered'
        coevaluationsheet.save()
    if coev_id:
        team = WorkTeam.objects.filter(course=coevaluation.course, wt_members__student=user).first()
        members = TeamMember.objects.filter(work_team=team)
        aviable = {}
        # for member in members:
        #     if member.student != user:
        #         cs = CoevaluationSheet.objects.filter(coevaluation_id=coev_id, coevaluator=user,
        #                                               coevaluated_id=int(member.student.pk)).first()
        #         print(member, user)
        #         print(member.student.pk)
        #         aviable[member.student.pk] = cs.status
        # Hacer un diccionario guardando los status , luego pasarle el coso y consultarlo en el hmlt
        # Como dict[a.id]
        current_st = -1
        if int(st_id) >= 0:
            a = members.filter(student_id=st_id).first().student
            if not a.get_full_name() == user.get_full_name():
                current_st = a

        context = {'coev': coevaluation,
                   "group": members,
                   "team": team,
                   "questions": questions,
                   "current_st": current_st,
                   "user": user,
                   "coevsheet": coevaluationsheet,
                  # "aviable": aviable
        }

        return render(request, 'coevaluador/studentCoevaluation.html', context)
    else:
        form = LoginForm()
        return render(request, 'coevaluador/login.html', {'form': form})


def teaching_coevaluation(request):
    return render(request, 'coevaluador/teachingCoevaluation.html')


def course(request, year, semester, code, section):
    user = request.user
    if user.is_authenticated:
        try:

            course_obj = Course.objects.get(year=year, semester=semester, code=code, section=section)

            print(year, semester, code, section)

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
                context['coevaluations'] = coevaluations.order_by('e_date').reverse()
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
