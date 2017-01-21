from django.conf.urls import url
from . import views

#app_name = 'task'
urlpatterns = [
    url(r'^sprint/$', views.sprint_overview, name='sprint_overview'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/$', views.sprint_detail, name='sprint_detail'),
    url(r'^task/$',views.task_index, name='task_overview'),
    url(r'^task/(?P<task_id>[0-9]+)/add/$', views.add_task,name='add_task'),
    url(r'^task/(?P<task_id>[0-9]+)/$', views.view_task,name= 'task_detail'),
    url(r'^$', views.overview, name='overview'),
    url(r'^groups/', views.group_list, name='group_list'),
]
