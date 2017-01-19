from django.conf.urls import url

from . import views

#app_name = 'task'
urlpatterns = [
    url(r'^sprint/$', views.sprint_overview, name='sprint_overview'),
    url(r'^sprint/(?P<sprint_id>[0-9]+)/$', views.sprint_detail, name='sprint_detail'),
   # url(r'^$',views.task_index, name='task_index'),
    url(r'^(?P<task_id>[0-9]+)/view/$', views.add_task),
    url(r'^(?P<task_id>[0-9]+)/$', views.view_task,name= 'detail'),
]
