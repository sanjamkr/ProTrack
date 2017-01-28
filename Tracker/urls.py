from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'), #1st login screen
    url(r'^homepage/$', views.homepage, name='homepage'), #Member page, shows list of groups
    
    url(r'^add_group/$',views.add_group, name='add_group'), 
    url(r'^add_project/$',views.add_project, name='add_project'),
    url(r'^add_task/$',views.add_task, name='add_task'),
    url(r'^add_sprint/$',views.add_sprint, name='add_sprint'),

    url(r'^edit_group/(?P<group_id>[0-9]+)/$',views.edit_group, name='edit_group'),
    url(r'^edit_project/(?P<project_id>[0-9]+)/$',views.edit_project, name='edit_project'),
    url(r'^edit_task/(?P<task_id>[0-9]+)/$',views.edit_task, name='edit_task'),
    url(r'^edit_sprint/(?P<sprint_id>[0-9]+)/$',views.edit_sprint, name='edit_sprint'),
    ]

