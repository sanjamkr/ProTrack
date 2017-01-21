from django.shortcuts import get_object_or_404, render
from django.http import Http404,HttpResponse

from Tracker.models import sprint

def sprint_detail(request,sprint_id):
    return HttpResponse("You're looking at sprint %s." % sprint_id)

