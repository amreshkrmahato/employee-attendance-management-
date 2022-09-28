import csv
from pyexpat import model
from tabnanny import verbose
from django.template import loader
from django.contrib import admin
from .models import Department,Admin,Class,Projects,Employees,Faculty,Calender,Projects,Attendance,Timetable,Mattendences
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib import messages
from django.urls import path
from django.db import models


admin.site.site_header = 'ADMIN ACCOUNT'
admin.site.site_title = 'Employee Attendance |'
admin.site.index_title = ""

class AttendanceD(models.Model):
    class Meta:
        verbose_name_plural = 'Attendance Report'
        app_label = 'login'

def my_custom_view(request):
    a=[1]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="AttendanceReport.csv"'
    atte=Attendance.objects.all().order_by('emply_id','project_id','date')
    writer = csv.writer(response)
    writer.writerow(['Emply-Id','Faculty-Id','Dept','Project-Id','Date(dd-mm-yyyy)','Status'])
    for i in atte:
        if i.presence:
            writer.writerow([i.emply_id.emply_id,i.fac_id.fac_id,i.emply_id.dept_id.dept_id,i.project_id.project_id,i.date,'Present'])
        else:
            writer.writerow([i.emply_id.emply_id,i.fac_id.fac_id,i.emply_id.dept_id.dept_id,i.project_id.project_id,i.date,'Absent'])
    return response

class DummyModelAdmin(admin.ModelAdmin):
    model = AttendanceD
    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('my_admin_path/', my_custom_view, name=view_name),
        ]

class EmplyAdmin(admin.ModelAdmin):
    list_display= ['emply_id',
'e_password',
'in_out',
'f_name',
'l_name',
'dept_id',
'class_id']
    list_editable = ['e_password','f_name','l_name','dept_id','class_id']
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:
            fields.remove('e_password')
        return fields

class FacAdmin(admin.ModelAdmin):
    list_display= ['fac_id','f_password','f_name','l_name','dept_id']
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj:
            fields.remove('f_password')
        return fields


admin.site.register(Employees,EmplyAdmin)
admin.site.register(AttendanceD, DummyModelAdmin)
admin.site.register(Department)
admin.site.register(Class)
admin.site.register(Faculty,FacAdmin)
admin.site.register(Calender)
admin.site.register(Projects)
admin.site.register(Attendance)
admin.site.register(Timetable)
admin.site.register(Mattendences)
admin.site.unregister(User)
admin.site.unregister(Group)
