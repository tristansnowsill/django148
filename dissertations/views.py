from django.db.models import Count
from django.shortcuts import render
from django.views import generic

from .models import Student, Supervisor

def home(request):
    return render(request, 'dissertations/base.html')

class StudentIndexView(generic.ListView):
    model = Student
    template_name = 'dissertations/student_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check whether any students don't have any supervisors
        if Student.objects.filter(supervisors__isnull=True):
            context['students_without_supervisors'] = Student.objects.filter(supervisors__isnull=True).all()
        return context

class SupervisorIndexView(generic.ListView):
    model = Supervisor
    template_name = 'dissertations/supervisor_list.html'

