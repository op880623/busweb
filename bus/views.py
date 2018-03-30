import json

from django.http import JsonResponse
from django.shortcuts import render

from bus.models import Bus, Stop

def map(request):
    data = {
        'name': '公車地圖',
        'thisStop': 'null',
        'data': {}
    }
    return render(request, 'bus/map.html', data)

def departure_map(request, uid):
    data = {
        'name': '從 %s 出發' % Stop.get(uid).name,
        'thisStop': thisStop(uid),
        'data': connected_stops(uid, True, False)
    }
    return render(request, 'bus/map.html', data)

def destination_map(request, uid):
    data = {
        'name': '前往 %s ' % Stop.get(uid).name,
        'thisStop': thisStop(uid),
        'data': connected_stops(uid, False, True)
    }
    return render(request, 'bus/map.html', data)

def connected_map(request, uid):
    data = {
        'name': '前往或從 %s 出發' % Stop.get(uid).name,
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


def thisStop(uid):
    return Stop.get(uid).to_hash()

def connected_stops(uid, departure=False, destination=False):
    stop = Stop.get(uid)
    data = {}
    if departure:
        for bus in stop.busses():
            for uid in bus.stops_id_after_stop(stop.uid):
                if uid not in data:
                    data[uid] = Stop.get(uid).to_hash()
                if 'departure' not in data[uid]:
                    data[uid]['departure'] = []
                data[uid]['departure'].append(bus.name)
    if destination:
        for bus in stop.busses():
            for uid in bus.stops_id_before_stop(stop.uid):
                if uid not in data:
                    data[uid] = Stop.get(uid).to_hash()
                if 'destination' not in data[uid]:
                    data[uid]['destination'] = []
                data[uid]['destination'].append(bus.name)
    return json.dumps(data)
