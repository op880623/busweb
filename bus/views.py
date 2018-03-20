from django.http import JsonResponse

from bus.models import Bus, Stop


def all_stops(request):
    data = {
        'stop': {},
        'route': {}
    }
    for stop in Stop.objects.all():
        data['stop'][stop.uid] = stop.to_hash()
    for bus in Bus.objects.all():
        data['route'][bus.uid] = bus.name
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
