from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect

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

def homepage(request):
    group_list = group.objects.order_by('id')[:]
    context = {
        'group_list': group_list,
    }
    return render(request,'Tracker/homepage.html',context)

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

#......Searching by tags................

def search_tag(request):
    tag_name = request.POST.get('textfield', None)
    try:
        user = tag.objects.get(tag = tag_name)
        html = ("<h1>Tasks Associated With Tag</h1>", user.task)
        return HttpResponse(html)
    except tag.DoesNotExist:
        return HttpResponse("There is no task associated with this tag")  

#..............Pie Chart..................
        
def pieview(request,project_id):
    open_tasks = 0
    complete_tasks = 0
    blocked_tasks = 0
    q = task.objects.filter(tproject = project_id)
    for e in q:
        if e.state == 'open':
            open_tasks = open_tasks + 1
        elif e.state == 'completed':
            complete_tasks = complete_tasks + 1
        elif e.state == 'blocked':
            blocked_tasks = blocked_tasks + 1
    context = { 'complete_tasks': complete_tasks, 
        'blocked_tasks': blocked_tasks, 
        'open_tasks': open_tasks
    }
    if complete_tasks>0 or blocked_tasks>0 or open_tasks>0:
        return render(request, 'Tracker/charts.html', context)
    else:
        return render(request, 'Tracker/nochart.html', context)
