from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
#from datetime import datetime, timezone, timedelta
from dateutil.rrule import rrule, MONTHLY, DAILY, YEARLY
from datetime import datetime, timedelta
from django.utils import timezone 
from Tracker.forms import NewTask,NewComment,NewTag,NewSprint
from django.contrib.auth.models import User, Group
from Tracker.models import project,sprint,task,tag
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
    open_tasks = 0
    complete_tasks = 0
    blocked_tasks = 0
    open_tp = 0
    complete_tp = 0
    blocked_tp = 0
    errorchart = 0
    now = datetime.now(timezone.utc)
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
    elif datetime.date(today) >= sp.end_date:
        st ="Sprint has Ended" 
    else: 
        st=" "
    #...........Charts..........
    
    if (sp.start_date<=sp.end_date):
        days = (sp.end_date - sp.start_date).days
        months = [dt for dt in rrule(MONTHLY, dtstart=sp.start_date, until=sp.end_date)]
        dates = [dt for dt in rrule(DAILY, dtstart=sp.start_date, until=sp.end_date)]
        years = months = [dt for dt in rrule(YEARLY, dtstart=sp.start_date, until=sp.end_date)]
        errorchart = 0
        
    else:
        months = []
        dates = []
        years = []
        categories = []
        idealdata = []
        errorchart = 1

    for e in t:
        if e.state == 'open':
            open_tasks = open_tasks + 1
            open_tp = open_tp + e.tp
        elif e.state == 'completed':
            complete_tasks = complete_tasks + 1
            complete_tp = complete_tp + e.tp
        elif e.state == 'blocked':
            blocked_tasks = blocked_tasks + 1
            blocked_tp = blocked_tp + e.tp
            
    total_tasks = open_tasks + complete_tasks + blocked_tasks
    total_tps = open_tp + complete_tp + blocked_tp
    realdata = []
    
    for i in range(days+1):
        x = sum(e.tp for e in t if datetime.date(e.created) <= (sp.start_date + timedelta(days=i)))
        y = sum(e.tp for e in t if ((e.comp_time!=None) and (datetime.date(e.comp_time) <= (sp.start_date + timedelta(days=i) )) ))
        realdata.append(x-y)
        categories = [str(dt.day) + ' ' + dt.strftime("%b") for dt in dates]
        diff = int(round(total_tps/(days+1)))
        idealdata = [total_tps - (i*diff) for i in range(days+1)]
    if total_tasks==0:
        errorchart = 1
    context ={
        'sprint': sp,
        'form': form,
        'st': st,
        'user':user,
        'complete_tasks': complete_tasks, 
        'blocked_tasks': blocked_tasks, 
        'open_tasks': open_tasks,
        'days' : days,
        'months': months,
        'dates' : dates,
        'categories' : categories,
        'idealdata' : idealdata,
        'realdata': realdata,
        'errorchart': errorchart
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
