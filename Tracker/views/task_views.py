from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse

from Tracker.models import task

def task_index (request):
    task_list = task.objects.order_by('-due_date')[:]
    context = {
        'task_list': task_list,
    }
    return render(request,'Tracker/index.html',context)
    
def add_task(request,task_id):
    response = "task details for id : %s. are -"
    return HttpResponse(response % task_id)

def view_task(request,task_id):
    ta = get_object_or_404(task,pk=task_id)
    return render(request,'Tracker/detail.html',{'task': ta})
   
def handle(request,task_id):
    response = " %s"
    return HttpResponse(response % task_id)



