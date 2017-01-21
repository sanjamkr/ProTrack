from django.shortcuts import get_object_or_404, render
from django.http import Http404,HttpResponse

from Tracker.models import task
    

def add_task(request):
    return render(request,'Tracker/task_add.html')
   
def task_detail(request,task_id):
    ta = get_object_or_404(task,pk=task_id)
    return render(request,'Tracker/task_detail.html',{'task': ta})




