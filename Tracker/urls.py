from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from . import views
from Tracker.views import ProfileImageIndexView

from django.contrib import admin
admin.autodiscover()

from Tracker.views import ProfileImageView, ProfileDetailView



urlpatterns = [
    #Login
    url(r'^$', views.login, name='login'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^add_group/$',views.add_group, name='add_group'), 
    #Group
    url(r'^homepage/$', views.login_next, name='login_next'),
    url(r'^edit_group/(?P<group_id>[0-9]+)/(?P<member_id>[0-9]+)/$',views.edit_group, name='edit_group'),
    url(r'^add_project/(?P<group_id>[0-9]+)/$',views.add_project, name='add_project'),
    #Project
    url(r'^edit_project/(?P<project_id>[0-9]+)/$',views.edit_project, name='edit_project'),
    url(r'^delete_project/(?P<project_id>[0-9]+)/$',views.delete_project, name='delete_project'),
    url(r'^add_task/(?P<project_id>[0-9]+)/$',views.add_task, name='add_task'),
    url(r'^add_sprint/(?P<project_id>[0-9]+)/$',views.add_sprint, name='add_sprint'),
    url(r'^search_tag/$',views.search_tag, name='search_tag'),
    url(r'^chart/(?P<project_id>[0-9]+)/$',views.pieview, name='chart'),
    #Task
    url(r'^edit_task/(?P<task_id>[0-9]+)/$',views.edit_task, name='edit_task'),
    url(r'^delete_task/(?P<task_id>[0-9]+)/$',views.delete_task, name='delete_task'),
    url(r'^add_comment/(?P<task_id>[0-9]+)/$',views.add_comment, name='add_comment'),
    url(r'^add_tag/(?P<task_id>[0-9]+)/$',views.add_tag, name='add_tag'),
    #Sprint
    url(r'^edit_sprint/(?P<sprint_id>[0-9]+)/$',views.edit_sprint, name='edit_sprint'),
    url(r'^spchart/(?P<sprint_id>[0-9]+)/$',views.sprintchart, name='sprintchart'),
    url(r'^delete_sprint/(?P<sprint_id>[0-9]+)/$',views.delete_sprint, name='delete_sprint'),
	#Image
	url(r'^$', ProfileImageView.as_view(), name='home'),
    url(r'^upload/', ProfileImageView.as_view(), name='profile_image_upload'),
    url(
        r'^uploaded/(?P<pk>\d+)/$', ProfileImageView.as_view(),
        name='profile_image'),
    
	]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 


