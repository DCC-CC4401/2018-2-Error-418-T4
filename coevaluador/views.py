from django.contrib import messages
from django.contrib.auth import authenticate, login as lgi, logout as lgo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash

from .forms import *
from .models import *
from .utils import parse_course_name

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
        c_set = []
        for c in cst.order_by('e_date').reverse():
            c_sheets = CoevaluationSheet.objects.filter(coevaluation=c, coevaluator=user)
            if c_sheets.exists():
                status = 'answered'
                for cs in c_sheets.all():
                    if cs.status == 'not_answered':
                        status = 'not_answered'
                c_set.append([c, status])

        cau = Coevaluation.objects.filter(course__in=au)
        cai = Coevaluation.objects.filter(course__in=ai)
        cte = Coevaluation.objects.filter(course__in=te)
        coevaluations = cst.union(cau, cai, cte)
        questions = Question.objects.all()
        context = {
            'c_sheets': c_set,
            'coevaluations': coevaluations.order_by('e_date').reverse()[:11],
            'courses': courses.order_by('name'),
            'courses_as_student': user.courses_as_student.all(),
            'courses_as_auxiliary': user.courses_as_auxiliary.all(),
            'courses_as_aide': user.courses_as_aide.all(),
            'courses_as_teacher': user.courses_as_teacher.all(),
            'questions': questions
        }
        return render(request, 'coevaluador/home.html', context)
    else:
        form = LoginForm()
        return render(request, 'coevaluador/login.html', {'form': form})


# NO BORRAR AÚN!!!
def student_home(request):
    # coevs = Coevaluation.objects.all()
    # for c in coevs:
    #     wts = c.course.workteam_set.all()
    #     for wt in wts:
    #         mem = wt.wt_members.all()
    #         n = len(mem)
    #         for i in range(n):
    #             a = mem[i].student
    #             for j in range(n):
    #                 b = mem[j].student
    #                 if a == b:
    #                     continue
    #                 else:
    #                     r = random.Random()
    #                     if c.status != 'opened':
    #                         g = r.randint(50, 70) * 1.0 / 10
    #                         cs = CoevaluationSheet(team=wt, coevaluation=c,
    #                                                coevaluator=a, coevaluated=b, status='answered', grade=g)
    #                         cs.save()
    #                     else:
    #                         if r.randint(0, 1) == 1:
    #                             g = r.randint(50, 70) * 1.0 / 10
    #                             cs = CoevaluationSheet(team=wt, coevaluation=c,
    #                                                    coevaluator=a, coevaluated=b, status='answered', grade=g)
    #                             cs.save()
    #                         else:
    #                             cs = CoevaluationSheet(team=wt, coevaluation=c,
    #                                                    coevaluator=a, coevaluated=b)
    #                             cs.save()
    return render(request, 'coevaluador/studentHome.html')


def teaching_home(request):
    return render(request, 'coevaluador/teachingHome.html')


@login_required(login_url='/login')
def coevaluation(request, coev_id, st_id="-1"):
    user = request.user
    st_id = user.pk if st_id == -1 else st_id
    co_evaluation_sheet = CoevaluationSheet.objects.filter(coevaluation_id=coev_id, coevaluator=user,
                                                           coevaluated_id=st_id).first()
    co_evaluation = Coevaluation.objects.get(id=coev_id)
    questions = co_evaluation.question.all()

    if request.method == 'POST':
        for q in questions:
            ans = request.POST[str(q.id)]
            answer = Answer(coevaluation_sheet=co_evaluation_sheet, question=q, ans=ans)
            answer.save()
        co_evaluation_sheet.status = 'answered'
        co_evaluation_sheet.save()
    if coev_id:
        team = WorkTeam.objects.filter(course=co_evaluation.course, wt_members__student=user).first()
        members = TeamMember.objects.filter(work_team=team)
        available = {}
        for member in members:
            if member.student != user:
                cs = CoevaluationSheet.objects.filter(coevaluation_id=coev_id, coevaluator=user,
                                                      coevaluated_id=member.student.pk).first()

                available[member.student.pk] = cs.status

        current_st = -1
        if st_id != "-1":
            a = members.filter(student_id=st_id).first().student
            if not a.get_full_name() == user.get_full_name():
                current_st = a

        context = {'coev': co_evaluation,
                   "group": members,
                   "team": team,
                   "questions": questions,
                   "current_st": current_st,
                   "user": user,
                   "coevsheet": co_evaluation_sheet,
                   "available": available,
                   "range": range(1, 8)
                   }

        return render(request, 'coevaluador/studentCoevaluation.html', context)
    else:
        form = LoginForm()
        return render(request, 'coevaluador/login.html', {'form': form})


def teaching_coevaluation(request, coev_id):
    user = request.user
    coevaluation = Coevaluation.objects.get(id=coev_id)
    questions = coevaluation.question.all()

    if coev_id:
        team = WorkTeam.objects.filter(course=coevaluation.course, wt_members__student=user).first()
        members = TeamMember.objects.filter(work_team=team)
        available = {}
        for member in members:
            if member.student != user:
                cs = CoevaluationSheet.objects.filter(coevaluation_id=coev_id, coevaluator=user,
                                                      coevaluated_id=member.student.pk).first()
                available[member.student.pk] = cs.status

        context = {'coev': coevaluation,
                   "group": members,
                   "team": team,
                   "questions": questions,
                   "user": user,
                   "available": available,
                   "range": range(1, 8)
                   }

        return render(request, 'coevaluador/teachingCoevaluation.html', context)
    else:
        form = LoginForm()
        return render(request, 'coevaluador/login.html', {'form': form})


def add_co_evaluation(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            co_title = request.POST['co_title']
            if 'co_course' not in request.POST:
                course_year = request.POST['course_year']
                course_semester = request.POST['course_semester']
                course_name = request.POST['course_name']
                course_section = request.POST['course_section']
                course_obj = Course.objects.get(year=course_year, semester=course_semester, name=course_name,
                                                section=course_section)
            else:
                course_str = request.POST['co_course']
                course_data = parse_course_name(course_str)
                len_cd = len(course_data)
                course_year = int(course_data[len_cd - 2])
                course_semester = int(course_data[len_cd - 1])
                course_code = course_data[0]
                course_section = int(course_data[1])
                course_obj = Course.objects.get(year=course_year, semester=course_semester, code=course_code,
                                                section=course_section)
            print("hola")
            questions_id = request.POST.getlist('co_questions')
            for i in questions_id:
                print(i)
            s_date = request.POST['co_s_date']
            e_date = request.POST['co_e_date']
            co_evaluation = Coevaluation(name=co_title, s_date=s_date, e_date=e_date,
                                         course=course_obj)
            co_evaluation.save()
            for q in questions_id:
                question = Question.objects.get(id=q)
                print(question)
                co_evaluation.question.add(question)
            co_evaluation.save()
            wts = co_evaluation.course.workteam_set.all()
            for wt in wts:
                mem = wt.wt_members.all()
                n = len(mem)
                for i in range(n):
                    a = mem[i].student
                    for j in range(n):
                        b = mem[j].student
                        if a == b:
                            continue
                        else:
                            cs = CoevaluationSheet(team=wt, coevaluation=co_evaluation, coevaluator=a, coevaluated=b)
                            cs.save()
            if 'co_course' not in request.POST:
                return HttpResponseRedirect(reverse('coevaluador:course',
                                                    args=(course_obj.year, course_obj.semester, course_obj.code,
                                                          course_obj.section)))
            else:
                return HttpResponseRedirect(reverse('coevaluador:home'))


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
                c_set = []
                for c in co_ev.order_by('e_date').reverse():
                    c_sheets = CoevaluationSheet.objects.filter(coevaluation=c, coevaluator=user)
                    if c_sheets.exists():
                        status = 'answered'
                        for cs in c_sheets.all():
                            if cs.status == 'not_answered':
                                status = 'not_answered'
                        c_set.append([c, status])
                context['coevaluations'] = co_ev.order_by('e_date').reverse()
                context['c_sheets'] = c_set
                return render(request, 'coevaluador/studentCourse.html', context)
            else:
                coevaluations = Coevaluation.objects.filter(course=course_obj)
                published_coevaluations = coevaluations.filter(status='Publicada')
                context['coevaluations'] = coevaluations.order_by('e_date').reverse()
                context['published_co_evs'] = published_coevaluations.order_by('s_date')
                work_teams = course_obj.workteam_set.all()
                wts = []
                for wt in work_teams:
                    members = wt.wt_members.all()
                    wt_mem = []
                    for m in members:
                        wt_mem.append(m)
                    wt_arr = [wt, wt_mem]
                    wts.append(wt_arr)
                context['work_teams'] = wts
                questions = course_obj.questions
                context['questions'] = questions.all()
                return render(request, 'coevaluador/teachingCourse.html', context)

        except Course.DoesNotExist:
            HttpResponseRedirect(reverse('coevaluador:login'))
    return HttpResponseRedirect(reverse('coevaluador:login'))


def student_course(request):
    return render(request, 'coevaluador/studentCourse.html')


def teaching_course(request):
    return render(request, 'coevaluador/teachingCourse.html')


def owner_profile(request):
    if request.user.is_authenticated:
        user = request.user
        st = user.courses_as_student.all()
        au = user.courses_as_auxiliary.all()
        ai = user.courses_as_aide.all()
        te = user.courses_as_teacher.all()
        courses = st.union(au, ai, te)
        coevaluated_sheets = user.coevaluated.all()
        coevaluations = list()
        coev_sheets = list()
        count = list()
        grade_sum = list()
        for c in coevaluated_sheets:
            if c.coevaluation.status == 'published':
                if c.coevaluation.name not in coevaluations:
                    coevaluations.append(c.coevaluation.name)
                    coev_sheets.append(c)
                    count.append(0)
                    grade_sum.append(0)
                i = coevaluations.index(c.coevaluation.name)
                count[i] += 1
                grade_sum[i] += float(c.grade)

        for index in range(len(grade_sum)):
            grade_sum[index] /= count[index]
            coev_sheets[index].grade = round(grade_sum[index], 1)
        form = ChangePasswordForm()
        context = {
            "student": user,
            "courses": courses,
            'courses_as_student': st,
            'courses_as_auxiliary': au,
            'courses_as_aide': ai,
            'courses_as_teacher': te,
            'coevaluated_sheets': coev_sheets,
            'form': form
        }
        return render(request, 'coevaluador/ownerProfile.html', context)
    else:
        form = LoginForm()
        return render(request, 'coevaluador/login.html', {'form': form})


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('coevaluador:ownerProfile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'coevaluador/changePassword.html', {
        'form': form
    })


def teaching_profile(request):
    return render(request, 'coevaluador/teachingProfile.html')
