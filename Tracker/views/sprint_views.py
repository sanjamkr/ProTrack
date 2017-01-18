from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from Tracker.models import sprint

def sprint_overview(request):
    sprint_list = sprint.objects.order_by('start_date')[:5]
    template = loader.get_template('Tracker/sprint_overview.html')
    context = {
        'sprint_list': sprint_list,
    }
    return HttpResponse(template.render(context, request))


def sprint_detail(request,sprint_id):
    return HttpResponse("You're looking at sprint %s." % sprint_id)

