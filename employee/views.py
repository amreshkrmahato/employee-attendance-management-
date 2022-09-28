import csv
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,redirect
from login.models import Department,Admin,Class,Employees,Faculty,Calender,Projects,Attendance,Timetable,Mattendences
from django.contrib import messages

# Create your views here.
emp=""
dep=""
cla=""
pro=""

def initial(emply,dept):
    global emp,dep
    emp=emply
    dep=dept
    return

def tial(clat,cout):
    global cla,pro
    cla=clat
    pro=cout
    print(clat)
    print(cout)
    return

def emplylogin(request):
    if request.method=="POST":
        u,p=request.POST.get('email'),request.POST.get('password')
        emply=Employees.objects.filter(emply_id=u)
        if emply.exists():
            if emply.get().e_password==p:
                d=emply.get().dept_id.dept_id
                initial(u,d)
                return emplyindex(request)
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('index')
        else:
            messages.error(request, 'No such User exists')
            return redirect('index')
    else:
        messages.error(request, 'Enter Credentials')
        return redirect('index')

def emplyprofile(request):
    if request.method=="POST":
        try:
            emply=Employees.objects.filter(emply_id=emp)
            fn=request.POST.get('fn')
            ln=request.POST.get('ln')
            pa=request.POST.get('pass')
            if fn != "":
                Employees.objects.filter(emply_id=emp).update(f_name=fn)
            if ln !="" :
                Employees.objects.filter(emply_id=emp).update(l_name=ln)
            if pa !="" :
                Employees.objects.filter(emply_id=emp).update(f_password=pa)
        except:
            messages.error(request, 'Oops something went wrong!')
            return redirect('emplyprofile')
    emply=Employees.objects.filter(emply_id=emp)
    print(emply)
    return render(request,'emplyprofile.html',{'emp':emply.get()})

def emplyindex(request):
    dept=Department.objects.filter(dept_id=dep)
    emply=Employees.objects.get(emply_id=emp)
    print(emply)
    atte=Attendance.objects.all().filter(emply_id=emply).order_by('-date')
    proj,pro=[],[]
    for i in atte:
        if i.project_id not in proj:
            proj.append(i.project_id)
    for i in proj:
        pro.append([i.project_id,0,Attendance.objects.all().filter(emply_id=emply,project_id=i.project_id).count(),0,i.project_name])
    for i in atte:
        for j in range(len(pro)):
            if i.project_id.project_id==pro[j][0]:
                if i.presence:
                    pro[j][1]+=1
    for i in pro:
        i[3]=int(i[1]/i[2]*100)
    proj=[]
    for i in pro:
        if i[3]<=40:
            pro.append(i)
    print('pro')
    return render(request,'emplyindex.html',{'emp':emply,'pro':pro})

def emplyadd(request):
    dept=Department.objects.filter(dept_id=dep)
    emply=Employees.objects.filter(emply_id=emp)
    atte=Attendance.objects.all().filter(emply_id=emp).order_by('-date')
    proj,pro=[],[]
    for i in atte:
        if i.project_id not in proj:
            proj.append(i.project_id)
    for i in proj:
        pro.append([i.project_id,0,Attendance.objects.all().filter(emply_id=emp,project_id=i.project_id).count(),0,i.project_name])
    for i in atte:
        for j in range(len(pro)):
            if i.project_id.project_id==pro[j][0]:
                if i.presence:
                    pro[j][1]+=1
    for i in pro:
        i[3]=int(i[1]/i[2]*100)
    print(pro)
    return render(request,'emplyadd.html',{'emply':emply,'pro':pro})

def emply_report(request):
    if request.method=="POST":
        dict=request.POST
        for i in dict.keys():
            if i!='csrfmiddlewaretoken':
                j=i
                break
        p=j
        tial(cla,p)
    a=[1]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="AttendanceReport.csv"'
    emply=Employees.objects.all().filter(emply_id=emp)
    atte=Attendance.objects.all().filter(project_id=pro,emply_id=emp).order_by('fac_id','date')
    writer = csv.writer(response)
    writer.writerow(['Fac-Id','Class-Id','Dept','Project-Id','Date','Status'])
    for i in atte:
        if i.presence:
            writer.writerow([i.fac_id.fac_id,emply.get().class_id.class_id,emply.get().dept_id.dept_id,pro,i.date,'Present'])
        else:
            writer.writerow([i.fac_id.fac_id,emply.get().class_id.class_id,emply.get().dept_id.dept_id,pro,i.date,'Absent'])
    return response
