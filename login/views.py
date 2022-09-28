from signal import default_int_handler
from django.shortcuts import render,redirect
from .models import Department,Admin,Class,Employees,Faculty,Calender,Projects,Attendance,Timetable,Mattendences
from django .contrib import messages
from django .contrib.auth import logout

def logout_request(request):
    logout(request)
    messages.info(request,"You have Logged Out Sucessfully")
    return render(request,'index.html')

def index(request):
    return render(request,'index.html')