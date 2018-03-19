import json

from django.shortcuts import render
from django.http import HttpResponse

from bus.models import Bus, Stop


def all_stops(request):
    data = {}
    data['stop'] = {}
    for stop in Stop.objects.all():
        data['stop'][stop.uid] = stop.to_hash()
    data['route'] = {}
    for bus in Bus.objects.all():
        data['route'][bus.uid] = bus.name
    return HttpResponse(json.dumps(data))

def departure(request, uid):
    stop = Stop.get(uid)
    data = {}
    data['departure'] = [s for s in stop.stops_can_go()]
    return HttpResponse(json.dumps(data))

def destination(request, uid):
    stop = Stop.get(uid)
    data = {}
    data['destination'] = [s for s in stop.stops_can_come()]
    return HttpResponse(json.dumps(data))

def connected(request, uid):
    stop = Stop.get(uid)
    data = {}
    data['departure'] = [s for s in stop.stops_can_go()]
    data['destination'] = [s for s in stop.stops_can_come()]
    return HttpResponse(json.dumps(data))
