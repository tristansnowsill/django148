from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from django.forms import Textarea

from .models import (AcademicYear, Programme, ResearchMethod, ResearchTopic,
                     Student, StudentSupervisor, Supervisor)

# Register your models here.
admin.site.register(AcademicYear)
admin.site.register(Programme)
admin.site.register(ResearchMethod)
admin.site.register(ResearchTopic)

class StudentSupervisorInline(admin.TabularInline):
    model = StudentSupervisor
    autocomplete_fields = ('supervisor', )
    extra = 1

class SupervisorStudentInline(admin.TabularInline):
    model = Student.supervisors.through

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('research_question', ( 'topics', 'methods' ))
        }),
        ('Student details', {
            'classes': ('collapse',),
            'fields': (('family_name', 'given_name'), 'email', 'srs', 'programme', 'academic_year')
        })
    )
    # filter_horizontal = ('topics', 'methods')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'cols': 80, 'rows': 3})},
    }
    inlines = (StudentSupervisorInline, )
    list_display = ('id', 'family_name', 'given_name', 'programme')
    list_display_links = ('id', 'family_name', 'given_name')
    list_filter = ('academic_year', 'programme__name')
    ordering = ('family_name', 'given_name')

@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    inlines = (SupervisorStudentInline, )
    list_display = ('id', 'family_name', 'given_name')
    list_display_links = ('id', 'family_name', 'given_name')
    ordering = ('family_name', 'given_name')
    search_fields = ('given_name', 'family_name')
