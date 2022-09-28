import csv
import pandas as pd
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,redirect
from login.models import Department,Admin,Class,Employees,Faculty,Calender,Projects,Attendance,Timetable,Mattendences
from django.contrib import messages

# Create your views here.
fac=""
dep=""
cla=""
pro=""

def initial(fact,dept):
    global fac,dep
    fac=fact
    dep=dept
    return

def tial(clat,cout):
    global cla,pro
    cla=clat
    pro=cout
    return

def faclogin(request):
    if request.method=="POST":
        u,p=request.POST.get('email'),request.POST.get('password')
        faco=Faculty.objects.filter(fac_id=u)
        if faco.exists():
            if faco.get().f_password==p:
                d=faco.get().dept_id.dept_id
                initial(u,d)
                return updatedindex(request)
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('index')
        else:
            messages.error(request, 'No such User exists')
            return redirect('index')
    else:
        messages.error(request, 'Enter Credentials')
        return redirect('index')

def updatedprofile(request):
    if request.method=="POST":
        try:
            fact=Faculty.objects.filter(fac_id=fac)
            fn=request.POST.get('fn')
            ln=request.POST.get('ln')
            pa=request.POST.get('pass')
            if fn != "":
                Faculty.objects.filter(fac_id=fac).update(f_name=fn)
            if ln !="" :
                Faculty.objects.filter(fac_id=fac).update(l_name=ln)
            if pa !="" :
                Faculty.objects.filter(fac_id=fac).update(f_password=pa)
            di=fact.get().dept_id.dept_id
        except:
            messages.error(request, 'Oops something went wrong!')
            return redirect('updatedadd')
    faco=Faculty.objects.filter(fac_id=fac)
    dept=Department.objects.filter(dept_id=dep)
    matted=Mattendences.objects.filter(fac_id=fac)
    clas=[]
    for i in matted:
        clas.append([i.class_id.class_id,i.project_id.project_id])
    return render(request,'updatedprofile.html',{'clas':clas,'fac':faco.get(),'dept':dept.get()})

def editatt(request):
    dept=Department.objects.filter(dept_id=dep)
    faco=Faculty.objects.filter(fac_id=fac)
    matted=Mattendences.objects.filter(fac_id=fac)
    clao=Class.objects.filter(class_id=cla)
    couo=Projects.objects.filter(project_id=pro)
    emply=Employees.objects.all().filter(class_id=cla)
    atte=Attendance.objects.all().filter(project_id=pro,fac_id=fac).order_by('-date')
    if request.method=="POST":
        dict=request.POST
        for emply1 in emply:
            if emply1.emply_id in dict.keys():
                if dict.get('bate'):
                    try:
                        a=Attendance.objects.filter(emply_id=emply1,fac_id=faco.get(),project_id=couo.get(),date=dict.get('bate')).get()
                        if a.presence:
                            p=0
                        else:
                            p=1
                        Attendance.objects.filter(emply_id=emply1,fac_id=faco.get(),project_id=couo.get(),date=dict.get('bate')).update(presence=p)
                        messages.success(request, 'Attendance Edited.')
                    except:
                        print(dict.get('bate').exists())
                        messages.error(request, 'Value does not Exist')
                        return redirect('updatedadd')
    return redirect('updatedadd')

def updatedindex(request):
    dept=Department.objects.filter(dept_id=dep)
    faco=Faculty.objects.filter(fac_id=fac)
    matted=Mattendences.objects.filter(fac_id=fac)
    clas=[]
    for i in matted:
        clas.append([i.class_id.class_id,i.project_id.project_id])
    return render(request,'updatedindex.html',{'clas':clas,'matted':matted})

def updatedadd(request):
    dept=Department.objects.filter(dept_id=dep)
    faco=Faculty.objects.filter(fac_id=fac)
    matted=Mattendences.objects.filter(fac_id=fac)
    clas=[]
    for i in matted:
        clas.append([i.class_id.class_id,i.project_id.project_id])
    clao=Class.objects.filter(class_id=cla)
    couo=Projects.objects.filter(project_id=pro)
    emply=Employees.objects.all().filter(class_id=cla)
    atte=Attendance.objects.all().filter(project_id=pro,fac_id=fac).order_by('-date')
    if request.method=="POST":
        n=request.POST.get('classg')
        if n is not None:
            n,p=n[:n.find('$')],n[n.find('$')+1:]
            tial(n,p)
        dict=request.POST
        for emply1 in emply:
            if emply1.emply_id in dict.keys():
                p=0
            else:
                p=1
            if dict.get('bate'):
                try:
                    a=Attendance(emply_id=emply1,fac_id=faco.get(),project_id=couo.get(),date=dict.get('bate'),presence=p)
                    a.save()
                    messages.success(request, 'Attendance Added.')
                except:
                    messages.error(request, 'Value already Exists')
                    return redirect('updatedadd')
    clao=Class.objects.filter(class_id=cla)
    couo=Projects.objects.filter(project_id=pro)
    emply=Employees.objects.all().filter(class_id=cla)
    dept=Department.objects.filter(dept_id=dep)
    faco=Faculty.objects.filter(fac_id=fac)
    matted=Mattendences.objects.filter(fac_id=fac)
    if emply.exists():
        dept=emply.first().dept_id
    else:
        dept=dept.get()
    atte=Attendance.objects.all().filter(project_id=pro,fac_id=fac).order_by('-date')
    return render(request,'updatedadd.html',{'emply' : emply,'fac':faco.get(),'clat':clao.get(),'cout':couo.get(),'dept':dept,'atte':atte,'clas':clas})
    
def fac_report(request):
    if request.method=="POST":
        dict=request.POST
        for i in dict.keys():
            if i!='csrfmiddlewaretoken':
                j=i
                break
        n,p=j[:j.find('$')],j[j.find('$')+1:]
        tial(n,p)
    a=[1]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="AttendanceReport.csv"'
    emply=Employees.objects.all().filter(class_id=cla)
    atte=Attendance.objects.all().filter(project_id=pro,fac_id=fac).order_by('emply_id','date')
    writer = csv.writer(response)

    writer.writerow(['Emply-Id','Class-Id','Dept','Project-Id','Date','Status'])
    for i in atte:
        if i.emply_id in emply:
            if i.presence:
                writer.writerow([i.emply_id.emply_id,cla,dep,pro,i.date,'Present'])
            else:
                writer.writerow([i.emply_id.emply_id,cla,dep,pro,i.date,'Absent'])
    return response