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

def group_detail(request,group_id):
    gname = get_object_or_404(group,pk=group_id)
    context = {
        'group': gname,
    }
    return render(request,'Tracker/group_detail.html',context)

def add_group(request):
    if request.method == 'POST':
        form = NewGroup(request.POST)
        if form.is_valid():
            new_group = form.save()
            return HttpResponseRedirect('/Tracker/homepage/')
    else:
        form = NewGroup()
    return render(request, 'Tracker/add_group.html', {'form': form})


#.........Project Views..................

def project_detail(request,project_id):
    p = get_object_or_404(project,pk=project_id)
    context = {
        'project' : p,
    }
    return render(request,'Tracker/project_detail.html',context)

def add_project(request):
    if request.method == 'POST':
        form = NewProject(request.POST)
        if form.is_valid():
            new_project = form.save()
            return HttpResponseRedirect('/Tracker/homepage/')
    else:
        form = NewProject()
    return render(request, 'Tracker/add_project.html', {'form': form})
