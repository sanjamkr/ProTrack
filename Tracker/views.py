from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse

from .models import task

def index (request):
    # tasks = task.objects.order_by('-due_date')[:5]
    # context = {'task_list': tasks}
    # return render(request,'task/index.html',context)
    return HttpResponse("You're in task view")
    
def detail(request,task_id):
    #task = get_object_or_404(task,pk=task_id)
    return HttpResponse("You're looking at task %s." % task_id)
    #return render(request,'task/detail.html',{'task': task})

def tag(request,task_id):
    response = "tags for the task %s."
    return HttpResponse(response % task_id)

def comment(request,task_id):
    response = "comment %s."
    return HttpResponse(response % task_id)

