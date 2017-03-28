from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
#from datetime import datetime, timezone, timedelta
from datetime import datetime, timedelta
from django.utils import timezone 
from dateutil.rrule import rrule, MONTHLY, DAILY, YEARLY
from django.contrib.auth.models import User, Group
from Tracker.models import project,sprint,task,tag,notification
from Tracker.forms import NewSprint
from django.contrib.auth.decorators import login_required


from django.contrib.auth import authenticate, login, logout


@login_required
def add_sprint(request,project_id):
    if request.method == 'POST':
        form = NewSprint(request.POST)
        if form.is_valid():
            new_sprint = form.save()
            user = User.objects.get(username=request.user.username)
            g = request.user.groups.all()[0]            
            n = notification.objects.create(type='ns', membergroup=g, othermember = user.username, content=new_sprint.sname, urlid=new_sprint.id, read=False, noti_date = new_sprint.screated)
            return HttpResponseRedirect('/Tracker/edit_project/'+str(new_sprint.project.id)+'/')
    else:
        user = User.objects.get(username=request.user.username)
        p = get_object_or_404(project,pk=project_id)
        form = NewSprint(initial={'project':p})
    return render(request, 'Tracker/add_sprint.html', {'form': form,'project_id':project_id,'user':user})


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
    if datetime.date(today) >= sp.end_date:
        st ="Sprint has Ended" 
    elif tdays>0:
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
def delete_sprint(request,sprint_id):
    s = get_object_or_404(sprint,pk=sprint_id)
    p = get_object_or_404(project,pk=s.project.id)
    sprint.objects.filter(id=sprint_id).delete()
    return HttpResponseRedirect('/Tracker/edit_project/'+str(p.id)+'/')

