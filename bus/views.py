import json

from django.http import JsonResponse
from django.shortcuts import render

from bus.models import Bus, Stop

def map(request):
    data = {
        'busName': busName(),
        'thisStop': None,
        'data': {
            'departure': {},
            'destination': {}
        }
    }
    return render(request, 'bus/map.html', data)

def departure_map(request, uid):
    data = {
        'busName': busName(),
        'thisStop': thisStop(uid),
        'data': connected_stops(uid, True, False)
    }
    return render(request, 'bus/map.html', data)

def destination_map(request, uid):
    data = {
        'busName': busName(),
        'thisStop': thisStop(uid),
        'data': connected_stops(uid, False, True)
    }
    return render(request, 'bus/map.html', data)

def connected_map(request, uid):
    data = {
        'busName': busName(),
        'thisStop': thisStop(uid),
        'data': connected_stops(uid, True, True)
    }
    return render(request, 'bus/map.html', data)

def stop_list(request):
    east = float(request.GET.get('e'))
    west = float(request.GET.get('w'))
    south = float(request.GET.get('s'))
    north = float(request.GET.get('n'))
    data = {}
    stops = Stop.objects.filter(latitude__range=(south, north),
                                longitude__range=(west, east))
    for stop in stops:
        data[stop.uid] = stop.to_hash()
    return JsonResponse(data)


def busName():
    data = {}
    for bus in Bus.objects.all():
        data[bus.uid] = bus.name
    return data

def thisStop(uid):
    return Stop.get(uid).to_hash()

def connected_stops(uid, departure=False, destination=False):
    stop = Stop.get(uid)
    data = {
        'departure': {},
        'destination': {}
    }
    if departure:
        for uid in stop.stops_can_go():
            data['departure'][uid] = Stop.get(uid).to_hash()
    if destination:
        for uid in stop.stops_can_come():
            data['destination'][uid] = Stop.get(uid).to_hash()
    return json.dumps(data)
