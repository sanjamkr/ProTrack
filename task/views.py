from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse

from .models import Task

def index (request):
    tasks = Task.objects.order_by('-due_date')[:5]
    context = {'task_list': tasks}
    return render(request,'task/index.html',context)
    
def detail(request,task_id):
    task = get_object_or_404(Task,pk=task_id)
    return render(request,'task/detail.html',{'task': task})

def tag(request,task_id):
    response = "tags for the task %s."
    return HttpResponse(response % task_id)

def comment(request,task_id):
    response = "comments %s."
    return HttpResponse(response % task_id)
