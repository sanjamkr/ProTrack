from django.shortcuts import get_object_or_404, render
from django.http import Http404,HttpResponse,HttpResponseRedirect

from Tracker.models import sprint
from Tracker.forms import NewSprint

def add_sprint(request):
    if request.method == 'POST':
        form = NewSprint(request.POST)
        if form.is_valid():
            new_sprint = form.save()
            return HttpResponseRedirect('/Tracker/homepage/')
    else:
        form = NewSprint()
    return render(request, 'Tracker/add_sprint.html', {'form': form})
    
def edit_sprint(request):
    if request.method == 'POST':
        a = sprint.objects.get(pk=6)
        form = NewSprint(request.POST, instance=a)
        if form.is_valid():
            new_article = form.save()
            return HttpResponseRedirect('/Tracker/homepage/')
    else:
        form = NewSprint()
    return render(request, 'Tracker/add_sprint.html', {'form': form})

def added(request):
    new_sprint_name = request.POST['sname']
    return HttpResponse("New Sprint Name : %s" % new_sprint_name)

def sprint_detail(request,sprint_id):
    return HttpResponse("You're looking at sprint %s." % sprint_id)

