from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from Tracker.models import project,sprint,notification,task,tag, project_file
from django.contrib.auth import authenticate, login, logout
#from datetime import datetime, timezone, timedelta
from datetime import datetime, timedelta
from django.utils import timezone 
from dateutil.rrule import rrule, MONTHLY, DAILY, YEARLY
from Tracker.forms import NewProject, SignUpForm, NewFile
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
from django.utils.html import conditional_escape as esc
from django.views.generic import ListView
import operator
import re
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, DetailView, ListView

#............Login...............

def log(request):
    context = {
    }
    return render(request,'Tracker/login.html',context)

def login_next(request):
    name = request.POST.get('name', None)
    pwd = request.POST.get('pwd', None)
    user = authenticate(username=name, password=pwd)
    if user is not None:
        login(request, user)
        g = user.groups.all()[0]
        today = datetime.today()
        now = datetime.now()
        near_deadline = []
        over_due = []
        new_task = []
    
        nd_count = 0
        nt_count = 0
        od_count = 0
    
        is_member = Q(assign = user)
        is_open = Q(state = "open")
        is_blocked = Q(state = "blocked")
        
        all_tasks = task.objects.filter(is_member).order_by('due_date')
        t = task.objects.filter(is_member & (is_blocked | is_open))
        t_count = task.objects.filter(is_member & (is_blocked | is_open)).count()
        nt_task = task.objects.filter(is_member)
       
        for t1 in t:
            if ((t1.due_date - datetime.date(today) ).days <= 2 ):
                if (((t1.due_date - datetime.date(today) ).days >= 0 ) ):
                    near_deadline.append(t1)
                    nd_count = nd_count+1
                else:
                    over_due.append(t1)
                    od_count = od_count+1
            
        for t2 in nt_task:
            if(( datetime.date(today) - datetime.date(t2.created) ).days <= 2 ):
                new_task.append(t2)
                nt_count = nt_count+1
                
        user_tp = {}
        for member in g.user_set.all():
            is_m = Q(assign = member)
            mem_name=member
            completed_tp =0
            total_tp = 0
            tl = task.objects.filter(is_m)
            for ts in tl:
                total_tp=total_tp+ts.tp
                if ts.state=='completed':
                    completed_tp=completed_tp+ts.tp
            if total_tp==0:
                ratio=0
            else:
                ratio=completed_tp/total_tp
            user_tp[mem_name]=ratio
            #user_tp.append(ratio)
        
        noti = nd_count + od_count        
        context ={
            'group': g,
            'user': user,
            'task':t,
            'all_tasks':all_tasks,
            't_count':t_count,
            'near_deadline':near_deadline, 
            'nd_count':nd_count, 
            'new_task':new_task, 
            'nt_count':nt_count, 
            'od_count':od_count, 
            'over_due':over_due, 
            'noti':noti,
            'user_tp':user_tp,
        }
        return render(request,'Tracker/home.html',context)
    else:
        return HttpResponseRedirect('/Tracker/')

def log_end(request):
    logout(request)
    return HttpResponseRedirect('/Tracker/')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            email = form.cleaned_data['email']
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()
            group_name = request.POST.get('group',None)
            g = Group.objects.get(name=group_name) 
            g.user_set.add(user)
            user = authenticate(username=username, password=password)
            return redirect('log')
    else:
        form = SignUpForm()
    gl = Group.objects.all()
    context = {
        'groups':gl,
        'form':form,
    }
    return render(request, 'Tracker/signup.html',context)

#.....................Group..........................

def group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group',None)
        g = Group.objects.get(name=group_name) 
        g.user_set.add(request.user)
        return HttpResponseRedirect('/Tracker/home')
    else:
        gl = Group.objects.all()
        context = {
            'groups':gl,
        }
        return render(request, 'Tracker/group.html',context) 

def add_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group',None)
        g = Group.objects.create(name=group_name)
        g.save()
        return HttpResponseRedirect('/Tracker/signup')
    else:
        context = {
        }
        return render(request, 'Tracker/add_group.html',context)

@login_required
def home(request):
    user = User.objects.get(username=request.user.username)
    g = user.groups.all()[0]
    is_member = Q(assign = user)
    is_open = Q(state = "open")
    is_blocked = Q(state = "blocked")
    all_tasks = task.objects.filter(is_member).order_by('due_date')
    t = task.objects.filter(is_member & (is_blocked | is_open))
    t_count = task.objects.filter(is_member & (is_blocked | is_open)).count()
    nt_task = task.objects.filter(is_member)
    today = datetime.today()
    now = datetime.now()
    near_deadline = []
    over_due = []
    new_task = []
    
    nd_count = 0
    nt_count = 0
    od_count = 0
    
    for t1 in t:
        if ((t1.due_date - datetime.date(today) ).days <= 2 ):
            if (((t1.due_date - datetime.date(today) ).days >= 0 ) ):
                near_deadline.append(t1)
                nd_count = nd_count+1
            else:
                over_due.append(t1)
                od_count = od_count+1
            
    for t2 in nt_task:
        if(( datetime.date(today) - datetime.date(t2.created) ).days <= 2 ):
            new_task.append(t2)
            nt_count = nt_count+1
            
    noti = nd_count + od_count

    user_tp = {}
    for member in g.user_set.all():
        is_m = Q(assign = member)
        mem_name=member
        completed_tp =0
        total_tp = 0
        tl = task.objects.filter(is_m)
        for ts in tl:
            total_tp=total_tp+ts.tp
            if ts.state=='completed':
                completed_tp=completed_tp+ts.tp
        if total_tp==0:
            ratio=0
        else:
            ratio=completed_tp/total_tp
        user_tp[mem_name]=ratio
        #user_tp.append(ratio)

    context ={
        'group': g,
        'user': user,
        'task':t,
        'all_tasks':all_tasks,
        't_count':t_count, 
        'near_deadline':near_deadline, 
        'nd_count':nd_count, 
        'new_task':new_task, 
        'nt_count':nt_count, 
        'od_count':od_count, 
        'over_due':over_due, 
        'noti':noti,
        'user_tp': user_tp,
    }
    return render(request,'Tracker/home.html',context)

#.........Project Views..................

@login_required
def FileView(request,project_id):
    if request.method == 'POST':
        form = NewFile(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            p = get_object_or_404(project,pk=project_id)            
            user = User.objects.get(username=request.user.username)
            g = user.groups.all()[0]
            n = notification.objects.create(type='uf', membergroup=g, othermember = user.username, content=p.pname, urlid=p.id, read=False, noti_date = datetime.now())
            return HttpResponseRedirect('/Tracker/edit_project/'+project_id+'/')
    else:
        p = get_object_or_404(project,pk=project_id)
        user = User.objects.get(username=request.user.username)
        form = NewFile(initial={'fproject': p })
        return render(request, 'Tracker/file_form.html', {'form': form,'project':p,'user':user})

@login_required
def FilesList(request,project_id):
    p = get_object_or_404(project,pk=project_id)
    files = project_file.objects.filter(fproject = p)
    user = User.objects.get(username=request.user.username)
    return render(request, 'Tracker/view_files.html', {'project':p,'user':user,'files':files})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = NewProject(request.POST)        
        if form.is_valid():   
            user = User.objects.get(username=request.user.username)
            g = request.user.groups.all()[0]
            new_project = form.save()
            n = notification.objects.create(type='np', membergroup=g, othermember = user.username, content=new_project.pname, urlid=new_project.id, read=False, noti_date = new_project.pcreated)
            return HttpResponseRedirect('/Tracker/home')
    else:
        user = User.objects.get(username=request.user.username)
        g = request.user.groups.all()[0]
        form = NewProject(initial={'pgroup': g})
        return render(request, 'Tracker/add_project.html', {'form': form,'user':user})

@login_required
def edit_project(request,project_id):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        p = get_object_or_404(project,pk=project_id)
        form = NewProject(request.POST,instance=p)
        if form.is_valid():
            form.save()
    else:
        p = get_object_or_404(project,pk=project_id)
        form = NewProject(instance=p)

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
        'user':user,
      }
    return render(request, 'Tracker/edit_project.html', context)


@login_required
def delete_project(request,project_id):
    p = get_object_or_404(project,pk=project_id)
    project.objects.filter(id=project_id).delete()
    return HttpResponseRedirect('/Tracker/home/')

#..........................Project Analysis.............................
@login_required
def pieview(request,project_id):
    open_tasks = 0
    complete_tasks = 0
    blocked_tasks = 0
    open_tp = 0
    complete_tp = 0
    blocked_tp = 0
    errorchart = 0
    p = get_object_or_404(project,pk=project_id)
    q = task.objects.filter(tproject = project_id)
    days = 0
    months = []
    dates = []
    years = []
    categories = []
    idealdata = []
    
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

    now = datetime.now(timezone.utc)
    days = (p.pdeadline - p.pcreated).days
    if (total_tasks > 0):
        if (p.pcreated<=p.pdeadline):
            months = [dt for dt in rrule(MONTHLY, dtstart=p.pcreated, until=p.pdeadline)]
            dates = [dt for dt in rrule(DAILY, dtstart=p.pcreated, until=p.pdeadline)]
            years = months = [dt for dt in rrule(YEARLY, dtstart=p.pcreated, until=p.pdeadline)]
            errorchart = 0
        else:

            errorchart = 1

        for i in range(days+1):
            x = sum(e.tp for e in q if datetime.date(e.created) <= (datetime.date(p.pcreated) + timedelta(days=i)))
            y = sum(e.tp for e in q if (e.comp_time!=None) and (datetime.date(e.comp_time) <= (datetime.date(p.pcreated) + timedelta(days=i))))
            realdata.append(x-y)
            categories = [str(dt.day) + ' ' + dt.strftime("%b") for dt in dates]
            diff = int(round(total_tp/(days+1)))
            idealdata = [total_tp - (i*diff) for i in range(days+1)]

        
    
    '''elif days >= 365:
        categories = [dt.strftime("%b") + " '" + dt.strftime("%y") for dt in months]
    elif days > 730:
        categories = [str(dt.year) for dt in years]'''
        
    context = { 'project_id': project_id,
        'project': p,
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
    if total_tasks>0:
        return render(request, 'Tracker/charts.html', context)
    else:
        return render(request, 'Tracker/nochart.html', context)



#.................................Calendar View............................

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


@login_required
def calendar(request,project_id):
    p = get_object_or_404(project,pk=project_id)
    try:
        user = User.objects.get(username=request.user.username)
        is_member = Q(assign = user)
        is_project = Q(tproject = project_id)
        q2 = task.objects.filter(is_member & is_project)
        q = task.objects.filter(tproject = project_id)
        t = q.latest('due_date')
        year=t.due_date.year
        month=t.due_date.month
        my_tasks = q.order_by('due_date').filter(due_date__year=year, due_date__month=month)
        cal = Calendar(my_tasks).formatmonth(year,month)
        #return render_to_response('Tracker/calendar.html', {'calendar':(cal),})
        return render_to_response('Tracker/calendar.html', {'calendar': mark_safe(cal),'project':p,'project_id':project_id,'user':user,'year':year,'month':month})
    except task.DoesNotExist:
        return render(request, 'Tracker/nochart.html', {'project_id':project_id,'project':p})  


@login_required        
def calendar1(request,project_id,year,month):
    p = get_object_or_404(project,pk=project_id)
    year=int(year)
    month=int(month)
    if month<2: 
        month=12
        year=year-1
    else:
        month=month-1
    user = User.objects.get(username=request.user.username)
    is_member = Q(assign = user)
    is_project = Q(tproject = project_id)
    q2 = task.objects.filter(is_member & is_project)
    q = task.objects.filter(tproject = project_id)
    t = q.latest('due_date')


    my_tasks = q.order_by('due_date').filter(due_date__year=year, due_date__month=month)
    cal = Calendar(my_tasks).formatmonth(year,month)
    return render_to_response('Tracker/calendar.html', {'calendar': mark_safe(cal),'project':p,'project_id':project_id,'user':user,'year':year,'month':month})


@login_required
def calendar2(request,project_id,year,month):
    p = get_object_or_404(project,pk=project_id)
    year=int(year)
    month=int(month)
    if month>11:    
        month=1
        year=year+1
    else:
        month=month+1
    user = User.objects.get(username=request.user.username)
    is_member = Q(assign = user)
    is_project = Q(tproject = project_id)
    q2 = task.objects.filter(is_member & is_project)
    q = task.objects.filter(tproject = project_id)
    t = q.latest('due_date')


    my_tasks = q.order_by('due_date').filter(due_date__year=year, due_date__month=month)
    cal = Calendar(my_tasks).formatmonth(year,month)
    return render_to_response('Tracker/calendar.html', {'calendar': mark_safe(cal),'project':p,'project_id':project_id,'user':user,'year':year,'month':month})

#..............................Search....................................

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 


def get_query(query_string, search_fields):

    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

@login_required
def search(request):
    user = User.objects.get(username=request.user.username)
    g = user.groups.all()[0]
    is_member = Q(assign = user)
    is_group = Q(pgroup = g)
    is_group_task= Q(tproject__pgroup__id = g.id)
    is_group_sprint = Q(project__pgroup__id=g.id)
    is_group_tag = Q(task__tproject__pgroup__id = g.id)
    query_string = ''
    task_entries = None
    tag_entries = None
    project_entries = None
    sprint_entries = None
    
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        task_query = get_query(query_string, ['tname', 'desc',])
        project_query = get_query(query_string, ['pname', 'pdesc',])
        sprint_query = get_query(query_string, ['sname',])
        tag_query = get_query(query_string, ['tag',])
        
        
        task_entries = task.objects.filter(is_group_task & task_query).order_by('-created')
        project_entries = project.objects.filter(is_group & project_query).order_by('-pdeadline')
        sprint_entries = sprint.objects.filter(is_group_sprint & sprint_query).order_by('-start_date')
        tag_entries = tag.objects.filter(is_group_tag & tag_query)
        
    return render(request, 'Tracker/searchresults.html', { 'query_string': query_string, 'task_entries': task_entries, 'project_entries': project_entries, 'sprint_entries': sprint_entries, 'tag_entries': tag_entries })
@login_required
def search_tag(request):
    user = User.objects.get(username=request.user.username)
    g = user.groups.all()[0]
    is_group = Q(pgroup = g)
    is_group_tag = Q(task__tproject__pgroup__id = g.id)
    query_string = ''
    tag_entries=None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        tag_query = get_query(query_string, ['tag',])
        tag_entries = tag.objects.filter(is_group_tag & tag_query)
    return render(request, 'Tracker/searchresults.html', { 'query_string': query_string, 'tag_entries': tag_entries})



#...............Notification..............
@login_required
def notifications(request):
    user = User.objects.get(username=request.user.username)
    g = user.groups.all()[0]
    is_member = Q(member = user)
    is_group = Q(membergroup = g)
    is_not_othermember = Q(othermember = user.username)
    my_notis = notification.objects.filter(is_member | (is_group & ~(is_not_othermember))).order_by('-noti_create')
    context = { 'my_notis': my_notis,
    }
    return render(request, 'Tracker/notifications.html', context)
