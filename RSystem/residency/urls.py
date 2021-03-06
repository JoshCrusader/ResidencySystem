"""RSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from . import views
urlpatterns = [
    #-----STANDARD----#
    url(r'^home/', views.index, name='index'),
    url(r'register', views.register, name = 'register'),
    url(r'errorlogin', views.XD, name = 'errorlogin'),
    url(r'idontacceptu', views.XD2, name = 'idontacceptu'),
    #----ADMIN----#
    url(r'^superuser/', views.super, name='superuser'),
    url(r'AdminApproval/', views.requestApproval, name='approve'),
    url(r'TeamManagement/', views.teamManagement, name='teammanage'),
    url(r'AssignProject/', views.assignProject, name='assignproject'),
    url(r'ProjectManagement/', views.ProjectManagement, name='ProjectManagement'),
    url(r'project/(?P<Project_id>[0-9]+)/',views.viewProj,name='view_proj'),
    url(r'CubicleAssignment/', views.cubehw, name='CubicleAssignment'),
        #// AJAX admin \\#
    url(r'ajax/accept_user/', views.acceptu, name='accept_user'),
    url(r'ajax/reject_user/', views.rejectu, name='reject_user'),
    url(r'ajax/create_project/',views.createp,name='create_project'),
    url(r'ajax/checkObjective/',views.checkObject,name='check_objective'),
    url(r'ajax/create_team/',views.createt,name='create_team'),
    url(r'ajax/selected_team/',views.selectt,name='selected_team'),
    url(r'ajax/join_request/',views.joinrequest,name='join_request'),
    url(r'ajax/remove_request/',views.removerequest,name='remove_request'),
    url(r'ajax/Assign_proj/',views.assignproj,name='assign_proj'),
    url(r'ajax/selected_cubes/',views.selectc,name='selected_cubes'),
    url(r'ajax/change_cub/',views.change_cub,name='change_cub'),


    #----REGULAR_USER----#
    url(r'^homepage/', views.home, name='homepage'),
    url(r'MyAssignment/(?P<Project_id>[0-9]+)/',views.myproj,name='my_project'),
    url(r'^ManageSched/',views.ManageSched,name='ManageSched'),
    url(r'ajax/user_cub/',views.user_cub,name='user_cub'),
    #// AJAX User \\#
    url(r'ajax/add_progress/',views.addprogress,name='add_progress'),
    url(r'ajax/change_role/',views.changerole,name='change_role'),
    url(r'ajax/add_sched/',views.addsched,name='add_sched'),
    url(r'ajax/request_logout', views.request_logout, name = "request_logout")
]
