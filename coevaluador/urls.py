from django.urls import path

from . import views

app_name = 'coevaluador'

urlpatterns = [
    # This is not specified in Django coding, but please use dash separated names, example: hello-world
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('student-home', views.student_home, name='studentHome'),
    path('teaching-home', views.teaching_home, name='teachingHome'),
    path('coevaluation/<int:coev_id>/<str:st_id>/', views.coevaluation, name='coevaluation'),
    path('coevaluation/<int:coev_id>/', views.coevaluation, name='coevaluation'),
    path('add-coevaluation', views.add_co_evaluation, name='addCoevaluation'),
    path('course/<int:year>/<int:semester>/<str:code>/<int:section>', views.course, name='course'),
    path('teaching-coevaluation/<int:coev_id>/', views.teaching_coevaluation, name='teachingcoevaluation'),
    path('student-course', views.student_course, name='studentCourse'),
    path('teaching-course', views.teaching_course, name='teachingCourse'),
    path('owner-profile', views.owner_profile, name='ownerProfile'),
    path('password-change', views.change_password, name='changePassword'),
    path('teaching-profile', views.teaching_profile, name='teachingProfile'),
]
