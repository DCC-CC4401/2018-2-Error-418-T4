from django.shortcuts import render


# Use underscore separated words for views like hello_world.


def login(request):
    return render(request, 'coevaluador/login.html')


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
