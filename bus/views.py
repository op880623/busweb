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

def stop(request, uid):
    stop = Stop.get(uid)
    data = stop.to_hash()
    return JsonResponse(data)

def stop_list(request):
    east = float(request.GET.get('e'))
    west = float(request.GET.get('w'))
    south = float(request.GET.get('s'))
    north = float(request.GET.get('n'))
    data = {}
    stops = Stop.objects.filter(latitude__range=(south, north),
                                longitude__range=(west, east))
    for stop in stops:
        data[stop.uid] = None
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
        for s in stop.stops_can_go():
            data['departure'][s] = None
    if destination:
        for s in stop.stops_can_come():
            data['destination'][s] = None
    return json.dumps(data)
