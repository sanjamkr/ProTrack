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

def task_detail(request,task_id):
    ta = get_object_or_404(task,pk=task_id)
    return render(request,'Tracker/task_detail.html',{'task': ta})




