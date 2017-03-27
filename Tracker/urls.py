from django.conf.urls import include, url
#from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    #Login
    url(r'^$',views.log, name='log'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^authentication/$', views.login_next, name='login_next'),
    url(r'^home/$',views.home,name='home'),
    url(r'^log_end/$',views.log_end,name='logout'),
    url(r'^add_group/$',views.add_group, name='add_group'),
    url(r'^group/$',views.group, name='group'),
    #Others
    url(r'^add_project/$',views.add_project, name='add_project'),
    url(r'^search/$', views.search, name ='search'),
    #Project
    url(r'^edit_project/(?P<project_id>[0-9]+)/$',views.edit_project, name='edit_project'),
    url(r'^delete_project/(?P<project_id>[0-9]+)/$',views.delete_project, name='delete_project'),
    url(r'^add_task/(?P<project_id>[0-9]+)/$',views.add_task, name='add_task'),
    url(r'^add_sprint/(?P<project_id>[0-9]+)/$',views.add_sprint, name='add_sprint'),
    url(r'^search_tag/$',views.search_tag, name='search_tag'),
    url(r'^chart/(?P<project_id>[0-9]+)/$',views.pieview, name='chart'),
    url(r'^calendar/(?P<project_id>[0-9]+)/$',views.calendar, name='calendar'),
    url(r'^calendar1/(?P<project_id>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$',views.calendar1, name='calendar1'),
    url(r'^calendar2/(?P<project_id>[0-9]+)/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$',views.calendar2, name='calendar2'),
    #Task
    url(r'^tsr/(?P<task_id>[0-9]+)/(?P<sprint_id>[0-9]+)/$',views.tsr, name='tsr'),
    url(r'^ts/(?P<task_id>[0-9]+)/(?P<sprint_id>[0-9]+)/$',views.ts, name='ts'),
    url(r'^edit_task/(?P<task_id>[0-9]+)/$',views.edit_task, name='edit_task'),
    url(r'^delete_task/(?P<task_id>[0-9]+)/$',views.delete_task, name='delete_task'),
    url(r'^add_comment/(?P<task_id>[0-9]+)/$',views.add_comment, name='add_comment'),
    url(r'^add_tag/(?P<task_id>[0-9]+)/$',views.add_tag, name='add_tag'),
    #Sprint
    url(r'^edit_sprint/(?P<sprint_id>[0-9]+)/$',views.edit_sprint, name='edit_sprint'),
    url(r'^delete_sprint/(?P<sprint_id>[0-9]+)/$',views.delete_sprint, name='delete_sprint'),
    #Image
    url(r'^upload/(?P<project_id>[0-9]+)/', views.FileView, name='file_upload'),
    url(r'^files/(?P<project_id>[0-9]+)/', views.FilesList, name='files'),
    ]
 
