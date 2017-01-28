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

def sprint_detail(request,sprint_id):
    s = get_object_or_404(sprint,pk=sprint_id)
    return render(request,'Tracker/sprint_detail.html',{'sprint': s})
