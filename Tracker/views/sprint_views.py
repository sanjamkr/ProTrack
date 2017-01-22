from django.shortcuts import get_object_or_404, render
from django.http import Http404,HttpResponse

from Tracker.models import sprint

def add_sprint(request):
    return render(request,'Tracker/add_sprint.html')

def added(request):
    new_sprint_name = request.POST['sname']
    return HttpResponse("New Sprint Name : %s" % new_sprint_name)

def sprint_detail(request,sprint_id):
    return HttpResponse("You're looking at sprint %s." % sprint_id)

