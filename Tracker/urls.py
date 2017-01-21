from django.conf.urls import url
from . import views

#app_name = 'task'
urlpatterns = [
    url(r'^$', views.login, name='login'), #1st login screen
    url(r'^MemberId=[0-9]+/$', views.homepage, name='homepage'), #Member page, shows list of groups
    url(r'^MemberId=[0-9]+/GroupId=(?P<group_id>[0-9]+)/$', views.group_detail, name='group_detail'), #Group details  #Includes list of projects
    url(r'^MemberId=[0-9]+/GroupId=[0-9]+/ProjectId=(?P<project_id>[0-9]+)/$', views.project_detail, name='project_detail'), #Project details,includes list of tasks & sprints
    url(r'^MemberId=[0-9]+/GroupId=[0-9]+/ProjectId=[0-9]+/TaskId=(?P<task_id>[0-9]+)/$', views.task_detail,name= 'task_detail'),
    url(r'^MemberId=[0-9]+/GroupId=[0-9]+/ProjectId=[0-9]+/SprintId=(?P<sprint_id>[0-9]+)/$', views.sprint_detail, name='sprint_detail'),

    url(r'^task/add_task/$',views.add_task, name='add_task'),
    ]
