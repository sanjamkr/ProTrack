from django.contrib.auth.models import User, Group
from django.shortcuts import render,get_object_or_404
from django.template import RequestContext, Template
from Tracker.models import notification
from django.db.models import Q
from django.http import HttpResponse,Http404,HttpResponseRedirect

def noti_count(request):
    noti_count = 0
    if request.user.is_authenticated:
        try:
            user = User.objects.get(username=request.user.username)
            if user.groups.all().exists():
                g = user.groups.all()[0]
                is_member = Q(member = user)
                is_group = Q(membergroup = g)
                is_not_othermember = Q(othermember = user.username)
                is_unread = Q(read = False)
    
                unread_notis = notification.objects.filter( is_unread & is_member  & ~(is_not_othermember) ).order_by('-noti_create')
                noti_count = unread_notis.count()
            else:
                pass
        except DoesNotExist:
            pass
    return{'noti_count': noti_count}
