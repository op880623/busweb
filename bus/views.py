from django.http import JsonResponse
from django.shortcuts import render

from bus.models import Bus, Stop

def map(request):
    return render(request, 'bus/map.html')

def departure_map(request, uid):
    return render(request, 'bus/map.html')

def destination_map(request, uid):
    return render(request, 'bus/map.html')

def connected_map(request, uid):
    return render(request, 'bus/map.html')

def bus_list(request):
    data = {}
    for bus in Bus.objects.all():
        data[bus.uid] = bus.name
    return JsonResponse(data)

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

def departure(request, uid):
    stop = Stop.get(uid)
    data = {'departure': [s for s in stop.stops_can_go()]}
    return JsonResponse(data)

def destination(request, uid):
    stop = Stop.get(uid)
    data = {'destination': [s for s in stop.stops_can_come()]}
    return JsonResponse(data)

def connected(request, uid):
    stop = Stop.get(uid)
    data = {
        'departure': [s for s in stop.stops_can_go()],
        'destination': [s for s in stop.stops_can_come()]
    }
    return JsonResponse(data)
