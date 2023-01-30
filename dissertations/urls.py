from django.urls import path

from . import views

app_name = 'dissertations'
urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.StudentIndexView.as_view(), name='students_index'),
    path('supervisors/', views.SupervisorIndexView.as_view(), name='supervisors_index'),
]