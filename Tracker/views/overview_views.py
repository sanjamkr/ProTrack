from django.shortcuts import render
from Tracker.models import group

from django.http import HttpResponse

def overview(request):
	return render(request, 'Tracker/overview.html', {})

def group_list(request):
	group_list = group.objects.order_by('id'),
	context = {
		'group_list': group_list,
	}
	return render(request, 'Tracker/group_list.html', context)


