from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from datetime import datetime, timezone, timedelta 
from dateutil.rrule import rrule, MONTHLY, DAILY, YEARLY
from Tracker.models import group,member,project,sprint,task,tag
from Tracker.forms import NewGroup,NewMember,NewProject

#...............Login..................

def login(request):
    context = {    
    }
    return render(request,'Tracker/login.html',context)

def login_next(request):
    name = request.POST.get('name', None)
    pwd = request.POST.get('pwd', None)
    try:
        user = member.objects.get(username = name,password = pwd)
        return edit_group(request,user.mgroup.id)
    except member.DoesNotExist:
        return HttpResponseRedirect('/Tracker/')
    
def signup(request):
    if request.method == 'POST':
        form = NewMember(request.POST)
        if form.is_valid():
            new_member = form.save()
            return HttpResponseRedirect('/Tracker/')
    else:
        form = NewMember()
    return render(request, 'Tracker/signup.html', {'form': form})

#............Group View.................

def add_group(request):
    if request.method == 'POST':
        form = NewGroup(request.POST)
        if form.is_valid():
            new_group = form.save()
            return HttpResponseRedirect('../../Tracker/signup')
    else:
        form = NewGroup()
    return render(request, 'Tracker/add_group.html', {'form': form})


def edit_group(request,group_id):
    g = get_object_or_404(group,pk=group_id)
    return render(request, 'Tracker/edit_group.html', {'group': g})

def delete_project(request,project_id):
    p = get_object_or_404(project,pk=project_id)
    g = get_object_or_404(group,pk=p.pgroup.id)
    project.objects.filter(id=project_id).delete()
    return HttpResponseRedirect('/Tracker/edit_group/'+str(g.id)+'/')

#.........Project Views..................

def add_project(request):
    if request.method == 'POST':
        form = NewProject(request.POST)
        if form.is_valid():
            new_project = form.save()
            return HttpResponseRedirect('/Tracker/edit_project/'+str(new_project.id)+'/')
    else:
        form = NewProject()
    return render(request, 'Tracker/add_project.html', {'form': form})

def edit_project(request,project_id):
    if request.method == 'POST':
        p = get_object_or_404(project,pk=project_id)
        form = NewProject(request.POST,instance=p)
        if form.is_valid():
            form.save()
    else:
        p = get_object_or_404(project,pk=project_id)
        form = NewProject(instance=p)
    return render(request, 'Tracker/edit_project.html', {'project': p,'form': form})

def search_tag(request):
    tag_name = request.POST.get('textfield', None)
    try:
        user = tag.objects.get(tag = tag_name)
        html = ("<h1>Tasks Associated With Tag</h1>", user.task)
        return HttpResponse(html)
    except tag.DoesNotExist:
        return HttpResponse("There is no task associated with this tag")  

def pieview(request,project_id):
    open_tasks = 0
    complete_tasks = 0
    blocked_tasks = 0
    open_tp = 0
    complete_tp = 0
    blocked_tp = 0
    p = get_object_or_404(project,pk=project_id)
    q = task.objects.filter(tproject = project_id)
    now = datetime.now(timezone.utc)
    days = (p.pdeadline - p.pcreated).days
    months = [dt for dt in rrule(MONTHLY, dtstart=p.pcreated, until=p.pdeadline)]
    dates = [dt for dt in rrule(DAILY, dtstart=p.pcreated, until=p.pdeadline)]
    years = months = [dt for dt in rrule(YEARLY, dtstart=p.pcreated, until=p.pdeadline)]

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
        x = sum(e.tp for e in q if e.created > (p.pcreated + timedelta(days=i)))
        y = sum(e.tp for e in q if (e.comp_time!=None) and (e.comp_time > (p.pcreated + timedelta(days=i))))
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
        return render(request, 'Tracker/charts.html', context)
    else:
        return render(request, 'Tracker/nochart.html', context)

