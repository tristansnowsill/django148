from django.db import models

class AcademicYear(models.Model):
    year            = models.CharField(max_length=16, default='2022/23')
    start_date      = models.DateField()
    report_deadline = models.DateField(null=True)

    def __str__(self):
        return self.year

class Programme(models.Model):
    code        = models.CharField(max_length=12)
    description = models.CharField(max_length=200)
    name        = models.CharField(max_length=200)

    def __str__(self):
        return '(%s) %s' % (self.code, self.description)

class ResearchTopic(models.Model):
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description

class ResearchMethod(models.Model):
    description = models.CharField(max_length=200)
    tag         = models.CharField(max_length=32)

    def __str__(self):
        return self.description

class Student(models.Model):
    given_name    = models.CharField(max_length=200)
    family_name   = models.CharField(max_length=200)
    email         = models.EmailField()
    srs           = models.CharField('Student Record System ID', max_length=11)
    parttime      = models.BooleanField('Part-time', default=False)
    distance      = models.BooleanField('Distance learner', default=False)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    programme     = models.ForeignKey(Programme, on_delete=models.CASCADE)
    
    research_question = models.TextField(blank=True)

    topics  = models.ManyToManyField(ResearchTopic, blank=True)
    methods = models.ManyToManyField(ResearchMethod, blank=True)

    supervisors = models.ManyToManyField('Supervisor', through='StudentSupervisor')

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return '%s %s' % (self.given_name, self.family_name)

    @property
    def NAME_full(self):
        return '%s, %s' % (str.upper(self.family_name), self.given_name)

class Supervisor(models.Model):
    given_name  = models.CharField(max_length=200)
    family_name = models.CharField(max_length=200)
    email       = models.EmailField()

    topics  = models.ManyToManyField(ResearchTopic, blank=True)
    methods = models.ManyToManyField(ResearchMethod, blank=True)

    # We don't define 'students' as a ManyToMany relationship because we only
    # define the relationship on one side

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return '%s %s' % (self.given_name, self.family_name)

    @property
    def NAME_full(self):
        return '%s, %s' % (str.upper(self.family_name), self.given_name)


class StudentSupervisor(models.Model):
    student    = models.ForeignKey(Student, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    confirmed  = models.BooleanField(default=True)
