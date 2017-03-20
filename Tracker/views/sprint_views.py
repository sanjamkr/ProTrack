from django.shortcuts import get_object_or_404, render
from django.http import Http404,HttpResponse,HttpResponseRedirect

from Tracker.models import sprint,project
from Tracker.forms import NewSprint

def add_sprint(request,project_id):
    if request.method == 'POST':
        form = NewSprint(request.POST)
        if form.is_valid():
            new_sprint = form.save()
            return HttpResponseRedirect('/Tracker/edit_project/'+str(new_sprint.project.id)+'/')
    else:
        p = get_object_or_404(project,pk=project_id)
        form = NewSprint(initial={'project':p})
    return render(request, 'Tracker/add_sprint.html', {'form': form,'project_id':project_id})

def edit_sprint(request,sprint_id):
    if request.method == 'POST':
        sp = get_object_or_404(sprint,pk=sprint_id)
        form = NewSprint(request.POST,instance=sp)
        if form.is_valid():
            form.save()
    else:
        sp = get_object_or_404(sprint,pk=sprint_id)
        form = NewSprint(instance=sp)
    return render(request, 'Tracker/edit_sprint.html', {'sprint': sp,'form': form})

def delete_sprint(request,sprint_id):
    s = get_object_or_404(sprint,pk=sprint_id)
    p = get_object_or_404(project,pk=s.project.id)
    sprint.objects.filter(id=sprint_id).delete()
    return HttpResponseRedirect('/Tracker/edit_project/'+str(p.id)+'/')
