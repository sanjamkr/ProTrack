from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'), #1st login screen
    url(r'^homepage/$', views.homepage, name='homepage'), #Member page, shows list of groups

    url(r'^Group=(?P<group_id>[0-9]+)/$', views.group_detail, name='group_detail'), #Group details  #Includes list of projects
    url(r'^Project=(?P<project_id>[0-9]+)/$', views.project_detail, name='project_detail'), #Project details #Includes list of tasks & sprints
    url(r'^Task=(?P<task_id>[0-9]+)/$', views.task_detail,name= 'task_detail'), #Task Details
    url(r'^Sprint=(?P<sprint_id>[0-9]+)/$', views.sprint_detail, name='sprint_detail'), #Sprint Details

    url(r'^add_group/$',views.add_group, name='add_group'), 
    url(r'^add_project/$',views.add_project, name='add_project'),
    url(r'^add_task/$',views.add_task, name='add_task'),
    url(r'^add_sprint/$',views.add_sprint, name='add_sprint'),
    ]
