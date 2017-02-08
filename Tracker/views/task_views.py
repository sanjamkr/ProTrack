from django.shortcuts import get_object_or_404, render
from django.http import Http404,HttpResponse,HttpResponseRedirect

from Tracker.models import task
from Tracker.forms import NewTask

def add_task(request):
    if request.method == 'POST':
        form = NewTask(request.POST)
        if form.is_valid():
            new_task = form.save()
            return HttpResponseRedirect('/Tracker/homepage/')
    else:
        form = NewTask()
    return render(request, 'Tracker/add_task.html', {'form': form})

def edit_task(request,task_id):
    if request.method == 'POST':
        t = get_object_or_404(task,pk=task_id)
        form = NewTask(request.POST,instance=t)
        if form.is_valid():
            form.save()
    else:
        t = get_object_or_404(task,pk=task_id)
        form = NewTask(instance=t)
    return render(request, 'Tracker/edit_task.html', {'task': t,'form': form})
    
def task_comment(request,task_id):
	tname = get_object_or_404(task,pk=task_id)
	return render(request,'Tracker/task_comment.html',{'task': tname})
