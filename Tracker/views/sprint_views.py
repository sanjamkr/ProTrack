from django.shortcuts import get_object_or_404, render
from django.http import Http404,HttpResponse,HttpResponseRedirect
from datetime import datetime, timezone, timedelta 
from dateutil.rrule import rrule, MONTHLY, DAILY, YEARLY
from Tracker.models import sprint,project,task
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

def sprintchart(request,sprint_id):
    open_tasks = 0
    complete_tasks = 0
    blocked_tasks = 0
    open_tp = 0
    complete_tp = 0
    blocked_tp = 0
    p = get_object_or_404(sprint,pk=sprint_id)
    q = task.objects.filter(tsprint = sprint_id)
    now = datetime.now(timezone.utc)
    days = (p.end_date - p.start_date).days
    months = [dt for dt in rrule(MONTHLY, dtstart=p.start_date, until=p.end_date)]
    dates = [dt for dt in rrule(DAILY, dtstart=p.start_date, until=p.end_date)]
    years = months = [dt for dt in rrule(YEARLY, dtstart=p.start_date, until=p.end_date)]

    for e in q:
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
    total_tp = open_tp + complete_tp + blocked_tp
    realdata = []
    for i in range(days+1):
        x = sum(e.tp for e in q if datetime.date(e.created) > (p.start_date + timedelta(days=i)))
        y = sum(e.tp for e in q if (e.comp_time!=None) and (e.comp_time > (datetime.date(p.start_date) + timedelta(days=i))))
        realdata.append(x-y)
        categories = [str(dt.day) + ' ' + dt.strftime("%b") for dt in dates]
        diff = int(round(total_tp/(days+1)))
        idealdata = [total_tp - (i*diff) for i in range(days+1)]
    
    '''elif days >= 365:
        categories = [dt.strftime("%b") + " '" + dt.strftime("%y") for dt in months]
    elif days > 730:
        categories = [str(dt.year) for dt in years]'''
        
    context = { 'complete_tasks': complete_tasks, 
        'blocked_tasks': blocked_tasks, 
        'open_tasks': open_tasks,
        'days' : days,
        'months': months,
        'dates' : dates,
        'categories' : categories,
        'idealdata' : idealdata,
        'realdata': realdata
    }
    if total_tasks>0:
        return render(request, 'Tracker/spcharts.html', context)
    else:
        return render(request, 'Tracker/nochart.html', context)

