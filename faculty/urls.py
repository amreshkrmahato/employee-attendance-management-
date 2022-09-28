from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.faclogin, name='faclogin'),
    path('faculty/', views.updatedindex, name='updatedindex'),
    path('facultyp/', views.updatedprofile, name='updatedprofile'),
    path('facultya/', views.updatedadd, name='updatedadd'),
    path('facultye/', views.editatt, name='editatt'),
    path('facultyr/', views.fac_report, name='fac_report'),
]
