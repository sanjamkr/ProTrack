from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
#from datetime import datetime, timezone, timedelta
from datetime import datetime, timedelta
from django.utils import timezone 
from Tracker.models import task,project,sprint
from Tracker.forms import NewTask,NewComment,NewTag,NewSprint

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def add_task(request,project_id):
    if request.method == 'POST':
        form = NewTask(request.POST)
        if form.is_valid():
            new_task = form.save()
            return HttpResponseRedirect('/Tracker/edit_project/'+str(new_task.tproject.id)+'/')
    else:
        user = User.objects.get(username=request.user.username)
        p = get_object_or_404(project,pk=project_id)
        form = NewTask(initial={'tproject': p })
    return render(request, 'Tracker/add_task.html', {'form': form,'project':p,'user':user})

@login_required
def edit_task(request,task_id):
    if request.method == 'POST':
        t = get_object_or_404(task,pk=task_id)
        form = NewTask(request.POST,instance=t)
        if form.is_valid():
            form.save()
    else:
        t = get_object_or_404(task,pk=task_id)
        form = NewTask(instance=t)
    user = User.objects.get(username=request.user.username)
    today = datetime.today()
    days = (t.due_date - datetime.date(today)).days
    return render(request, 'Tracker/edit_task.html', {'task': t,'form': form, 'days': days,'user':user})

@login_required
def edit_sprint(request,sprint_id):
    if request.method == 'POST':
        sp = get_object_or_404(sprint,pk=sprint_id)
        form = NewSprint(request.POST,instance=sp)
        if form.is_valid():
            form.save()
    else:
        sp = get_object_or_404(sprint,pk=sprint_id)
        form = NewSprint(instance=sp)
    user = User.objects.get(username=request.user.username)
    completed_tp = 0
    total_tp = 0
    t = task.objects.filter(tsprint = sprint_id)
    for tk in t:
        if tk.state == 'completed':
            completed_tp = completed_tp + tk.tp
        total_tp = total_tp + tk.tp
    today = datetime.today()
    tdays = (sp.end_date - sp.start_date).days
    if tdays>0:
        pdays = (datetime.date(today) - sp.start_date).days
        ideal_tp = total_tp/tdays*pdays
        real_tp = completed_tp
        if ideal_tp <= real_tp:
            st = 'Green'
        elif ideal_tp <= real_tp+ideal_tp*0.3 :
            st = 'Yellow'
        else:
            st = 'Red'
    else:
        st ="Sprint has already ended" 
    context ={
        'sprint': sp,
        'form': form,
        'st': st,
        'user':user,
      }
    return render(request, 'Tracker/edit_sprint.html', context)

@login_required
def ts(request,task_id,sprint_id):
        s = get_object_or_404(sprint,pk=sprint_id)
        task.objects.filter(pk=task_id).update(tsprint=s)
        return edit_sprint(request,sprint_id)

@login_required
def tsr(request,task_id,sprint_id):
        task.objects.filter(pk=task_id).update(tsprint=None)
        return edit_sprint(request,sprint_id)

@login_required
def delete_task(request,task_id):
    t = get_object_or_404(task,pk=task_id)
    p = get_object_or_404(project,pk=t.tproject.id)
    task.objects.filter(id=task_id).delete()
    return HttpResponseRedirect('/Tracker/edit_project/'+str(p.id)+'/')

@login_required
def add_comment(request,task_id):
    if request.method == 'POST':
        form = NewComment(request.POST)
        if form.is_valid():
            new_comment = form.save()
            return HttpResponseRedirect('/Tracker/edit_task/'+str(new_comment.task.id)+'/')
    else:
        t = get_object_or_404(task,pk=task_id)
        user = User.objects.get(username=request.user.username)
        form = NewComment(initial={'task': t,'member':user})
    return render(request, 'Tracker/add_comment.html',{'form':form,'task_id':task_id})

@login_required
def add_tag(request,task_id):
    if request.method == 'POST':
        form = NewTag(request.POST)
        if form.is_valid():
            new_tag = form.save()
            return HttpResponseRedirect('/Tracker/edit_task/'+str(new_tag.task.id)+'/')
    else:
        t = get_object_or_404(task,pk=task_id)
        user = User.objects.get(username=request.user.username)
        form = NewTag(initial={'task': t })
    return render(request, 'Tracker/add_tag.html', {'form': form,'task_id':task_id,'user':user})
