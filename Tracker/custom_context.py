from django.contrib.auth.models import User, Group
from django.template import RequestContext, Template
from Tracker.models import notification
from django.db.models import Q
from django.http import HttpResponse,Http404,HttpResponseRedirect

def noti_count(request):
    user = User.objects.get(username=request.user.username)
    g = user.groups.all()[0]
    is_member = Q(member = user)
    is_group = Q(membergroup = g)
    is_not_othermember = Q(othermember = user.username)
    is_unread = Q(read = False)
    
    unread_notis = notification.objects.filter(is_unread & (is_member | (is_group & ~(is_not_othermember)))).order_by('-noti_create')
    noti_count = unread_notis.count()

    

    return{'noti_count': noti_count}