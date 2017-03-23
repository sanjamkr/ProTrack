from django.shortcuts import get_object_or_404, render
from django.http import Http404,HttpResponse,HttpResponseRedirect
#from datetime import datetime, timezone, timedelta
from datetime import datetime, timedelta
from django.utils import timezone 
from Tracker.models import task,project,member
from Tracker.forms import NewTask,NewComment,NewTag

def add_task(request,project_id,member_id):
    if request.method == 'POST':
        form = NewTask(request.POST)
        if form.is_valid():
            new_task = form.save()
            return HttpResponseRedirect('/Tracker/edit_project/'+str(new_task.tproject.id)+'/'+member_id+'/')
    else:
        p = get_object_or_404(project,pk=project_id)
        form = NewTask(initial={'tproject': p })
        m = get_object_or_404(member,pk=member_id)
    return render(request, 'Tracker/add_task.html', {'form': form,'project':p,'member':m})

def edit_task(request,task_id,member_id):
    if request.method == 'POST':
        t = get_object_or_404(task,pk=task_id)
        form = NewTask(request.POST,instance=t)
        if form.is_valid():
            form.save()
    else:
        t = get_object_or_404(task,pk=task_id)
        form = NewTask(instance=t)
    m = get_object_or_404(member,pk=member_id)
    today = datetime.today()
    days = (t.due_date - datetime.date(today)).days
    return render(request, 'Tracker/edit_task.html', {'task': t,'form': form, 'days': days,'member':m})

def delete_task(request,task_id,member_id):
    t = get_object_or_404(task,pk=task_id)
    p = get_object_or_404(project,pk=t.tproject.id)
    task.objects.filter(id=task_id).delete()
    return HttpResponseRedirect('/Tracker/edit_project/'+str(p.id)+'/'+member_id+'/')

def add_comment(request,task_id,member_id):
    if request.method == 'POST':
        form = NewComment(request.POST)
        if form.is_valid():
            new_comment = form.save()
            return HttpResponseRedirect('/Tracker/edit_task/'+str(new_comment.task.id)+'/'+member_id+'/')
    else:
        t = get_object_or_404(task,pk=task_id)
        m = get_object_or_404(member,pk=member_id)
        form = NewComment(initial={'task': t,'member':m})
    return render(request, 'Tracker/add_comment.html',{'form':form,'task_id':task_id,'member':m})

def add_tag(request,task_id,member_id):
    if request.method == 'POST':
        form = NewTag(request.POST)
        if form.is_valid():
            new_tag = form.save()
            return HttpResponseRedirect('/Tracker/edit_task/'+str(new_tag.task.id)+'/'+member_id+'/')
    else:
        t = get_object_or_404(task,pk=task_id)
        m = get_object_or_404(member,pk=member_id)
        form = NewTag(initial={'task': t })
    return render(request, 'Tracker/add_tag.html', {'form': form,'task_id':task_id,'member':m})
