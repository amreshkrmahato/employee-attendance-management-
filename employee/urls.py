from django.urls import path,include
from . import views


urlpatterns = [
    path('index/', views.emplylogin, name='emplylogin'),
    path('faculty/', views.emplyindex, name='emplyindex'),
    path('facultyp/', views.emplyprofile, name='emplyprofile'),
    path('facultya/', views.emplyadd, name='emplyadd'),
    path('facultyr/', views.emply_report, name='emply_report'),
]