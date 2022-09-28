from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



# Create your models here.

DAYS_CHOICE=[('mon','Monday'),('tue','Tuesday'),('wed','Wednesday'),('thu','Thursday'),('fri','Friday'),('sat','Saturday'),]
LEAVE_CHOICE=[('ml','Medical Leave'),('od','On Duty')]

class Department(models.Model):
    dept_id = models.CharField(max_length=20,primary_key = True)
    dept_name = models.CharField(max_length=50)

class Admin(models.Model):
    admin_id = models.CharField(max_length=20,primary_key = True)
    password =models.CharField(max_length=30)

class Class(models.Model):
    class_id = models.CharField(max_length=20,primary_key=True)
    total_employees = models.IntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(100)])

class Employees(models.Model):
    emply_id = models.CharField(max_length=20,primary_key=True)
    e_password = models.CharField(max_length=30)
    in_out = models.CharField(max_length=5)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

class Faculty(models.Model):
    fac_id = models.CharField(max_length=20,primary_key=True)
    f_password = models.CharField(max_length=30)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)

class Calender(models.Model):
    i=models.AutoField(primary_key=True)
    dates = models.DateField()
    day = models.CharField(max_length=9,choices=DAYS_CHOICE,default=None,blank=False)

class Projects(models.Model):
    project_id = models.CharField(max_length=20,primary_key=True)
    project_name = models.CharField(max_length=50)
    credits = models.IntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(5)])

class Attendance(models.Model):
    emply_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    fac_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    date = models.DateField()
    presence = models.IntegerField(validators=[MinValueValidator(0),
                                       MaxValueValidator(1)])
    class Meta:
        unique_together = (("emply_id", "project_id","date"),)

class Slot(models.Model):
    period_id=models.IntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(8)],primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

class Holiday(models.Model):
    date = models.DateField(primary_key=True)
    description = models.CharField(max_length=100)

class Advisor(models.Model):
    fac_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

class Timetable(models.Model):
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    day = models.CharField(max_length=9,choices=DAYS_CHOICE,default=None,blank=False)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    class Meta:
        unique_together = (("class_id", "project_id","day"),)

class Mattendences(models.Model):
    fac_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    class Meta:
        unique_together = (("project_id", "class_id"),)
