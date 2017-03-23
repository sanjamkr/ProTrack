from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
#from datetime import datetime, timezone, timedelta
from datetime import datetime, timedelta
from django.utils import timezone 
from dateutil.rrule import rrule, MONTHLY, DAILY, YEARLY
from Tracker.models import group,member,project,sprint,task,tag
from Tracker.forms import NewGroup,NewMember,NewProject
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
from django.utils.html import conditional_escape as esc
from django.db.models import Q


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
        return edit_group(request,user.mgroup.id,user.id)
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

def edit_group(request,group_id,member_id):
    g = get_object_or_404(group,pk=group_id)
    m = get_object_or_404(member,pk=member_id)
    is_member = Q(assign = member_id)
    is_open = Q(state = "open")
    is_blocked = Q(state = "blocked")
    all_tasks = task.objects.filter(is_member)
    t = task.objects.filter(is_member & (is_blocked | is_open))
    t_count = task.objects.filter(is_member & (is_blocked | is_open)).count()
    return render(request, 'Tracker/edit_group.html', {'group': g,'member':m, 'task':t, 'all_tasks':all_tasks, 't_count':t_count})

#.........Project Views..................

def add_project(request,group_id,member_id):
    if request.method == 'POST':
        form = NewProject(request.POST)
        if form.is_valid():
            new_project = form.save()
            return HttpResponseRedirect('/Tracker/edit_project/'+str(new_project.id)+'/'+member_id+'/')
    else:
        g = get_object_or_404(group,pk=group_id)
        m = get_object_or_404(member,pk=member_id)
        form = NewProject(initial={'pgroup': g})
    return render(request, 'Tracker/add_project.html', {'form': form,'group_id':group_id, 'member':m})

def edit_project(request,project_id,member_id):
    if request.method == 'POST':
        p = get_object_or_404(project,pk=project_id)
        form = NewProject(request.POST,instance=p)
        if form.is_valid():
            form.save()
    else:
        p = get_object_or_404(project,pk=project_id)
        form = NewProject(instance=p)
    m = get_object_or_404(member,pk=member_id)
    completed_tp = 0
    total_tp = 0
    t = task.objects.filter(tproject = project_id)
    for tk in t:
        if tk.state == 'completed':
            completed_tp = completed_tp + tk.tp
        total_tp = total_tp + tk.tp
    today = datetime.today()
    tdays = (p.pdeadline - p.pcreated).days
    pdays = (datetime.date(today) - datetime.date(p.pcreated)).days
    ideal_tp = total_tp/tdays*pdays
    real_tp = completed_tp
    if ideal_tp <= real_tp:
        ps = 'Green'
    elif ideal_tp <= real_tp+ideal_tp*0.3 :
        ps = 'Yellow'
    else:
        ps = 'Red'
    context ={
        'project': p,
        'form': form,
        'ps': ps,
        'member':m
      }
    return render(request, 'Tracker/edit_project.html', context)

def delete_project(request,project_id,member_id):
    p = get_object_or_404(project,pk=project_id)
    g = get_object_or_404(group,pk=p.pgroup.id)
    project.objects.filter(id=project_id).delete()
    return HttpResponseRedirect('/Tracker/edit_group/'+str(g.id)+'/'+member_id+'/')

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


class Calendar(HTMLCalendar):

    def __init__(self, my_tasks):
        super(Calendar, self).__init__()
        self.my_tasks = self.group_by_day(my_tasks)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.my_tasks:
                cssclass += ' filled'
                body = ['<ul class="sample">']
                for workout in self.my_tasks[day]:
                    body.append('<li>')
                    #body.append('<a href="%s">' % workout.get_absolute_url())
                    #body.append('<a href="Tracker/calendar1/">')
                    body.append(esc(workout.tname))
                    body.append('</a></li>')
                    #body.append('</li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')
	
    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(Calendar, self).formatmonth(year, month)

    def group_by_day(self,my_tasks):
        field = lambda workout: workout.due_date.day
        return dict(
            [(day, list(items)) for day, items in groupby(my_tasks, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


def calendar(request,project_id):
	q = task.objects.filter(tproject = project_id)
	t=q.earliest('due_date')
	year=t.due_date.year
	month=t.due_date.month
	my_tasks = q.order_by('due_date').filter(due_date__year=year, due_date__month=month)
	cal = Calendar(my_tasks).formatmonth(year, month)
	#return render_to_response('Tracker/calendar.html', {'calendar':(cal),})
	return render_to_response('Tracker/calendar.html', {'calendar': mark_safe(cal),})
	                   
