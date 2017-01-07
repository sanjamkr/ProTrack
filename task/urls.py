from django.conf.urls import url

from . import views

app_name = 'task'
urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^(?P<task_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<task_id>[0-9]+)/tags/$', views.tag, name='tag'),
    url(r'^(?P<task_id>[0-9]+)/comment/$', views.comment, name='comment'),   
]
