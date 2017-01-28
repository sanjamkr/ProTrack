from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect

from Tracker.models import group,project,task,sprint
from Tracker.forms import NewGroup,NewProject

#...............Login..................

def login(request):
    context = {    
    }
    return render(request,'Tracker/login.html',context)

def homepage(request):
    group_list = group.objects.order_by('id')[:]
    context = {
        'group_list': group_list,
    }
    return render(request,'Tracker/homepage.html',context)

#............Group Views.................

def add_group(request):
    if request.method == 'POST':
        form = NewGroup(request.POST)
        if form.is_valid():
            new_group = form.save()
            return HttpResponseRedirect('/Tracker/homepage/')
    else:
        form = NewGroup()
    return render(request, 'Tracker/add_group.html', {'form': form})

def edit_group(request,group_id):
    if request.method == 'POST':
        g = get_object_or_404(group,pk=group_id)
        form = NewGroup(request.POST,instance=g)
        if form.is_valid():
            form.save()
    else:
        g = get_object_or_404(group,pk=group_id)
        form = NewGroup(instance=g)
    return render(request, 'Tracker/edit_group.html', {'group': g,'form': form})

#.........Project Views..................

def add_project(request):
    if request.method == 'POST':
        form = NewProject(request.POST)
        if form.is_valid():
            new_project = form.save()
            return HttpResponseRedirect('/Tracker/homepage/')
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
