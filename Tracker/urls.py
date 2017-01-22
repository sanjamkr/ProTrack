from django.conf.urls import url
from . import views

#app_name = 'task'
urlpatterns = [
    url(r'^$', views.login, name='login'), #1st login screen
    url(r'^homepage/$', views.homepage, name='homepage'), #Member page, shows list of groups
    url(r'^GroupId=(?P<group_id>[0-9]+)/$', views.group_detail, name='group_detail'), #Group details  #Includes list of projects
    url(r'^ProjectId=(?P<project_id>[0-9]+)/$', views.project_detail, name='project_detail'), #Project details,includes list of tasks & sprints
    url(r'^TaskId=(?P<task_id>[0-9]+)/$', views.task_detail,name= 'task_detail'),
    url(r'^SprintId=(?P<sprint_id>[0-9]+)/$', views.sprint_detail, name='sprint_detail'),

    url(r'^task/add_task/$',views.add_task, name='add_task'),
    url(r'^sprint/add_sprint/$',views.add_sprint, name='add_sprint'),
    ]
