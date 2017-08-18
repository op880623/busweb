import shelve

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse

from .models import BusStop, BusRoute


dbRoute = 'busInfo/db/route'
dbStop = 'busInfo/db/stop'


def all_stops(request):
    stops = []
    with shelve.open(dbStop) as stopData:
        for stopId in stopData:
            stops.append(stopData[stopId])
    json = '{"type":"all","stops":[' + ','.join([stop.to_json() for stop in stops]) + ']}'
    return HttpResponse(json)


def departure(request, uid):
    with shelve.open(dbStop) as stopData:
        thisStop = stopData[uid]
    response_type = '"type":"departure"'
    stops = []
    with shelve.open(dbStop) as stopData:
        for stopId in thisStop.stops_can_go(dbRoute=dbRoute):
            stops.append(stopData[stopId].to_json())
    stops = '"stops":[' + ','.join(stops) + ']'
    json = '{' + ','.join([response_type, '"thisStop":' + thisStop.to_json(), stops]) + '}'
    return HttpResponse(json)


def destination(request, uid):
    with shelve.open(dbStop) as stopData:
        thisStop = stopData[uid]
    response_type = '"type":"destination"'
    stops = []
    with shelve.open(dbStop) as stopData:
        for stopId in thisStop.stops_can_come(dbRoute=dbRoute):
            stops.append(stopData[stopId].to_json())
    stops = '"stops":[' + ','.join(stops) + ']'
    json = '{' + ','.join([response_type, '"thisStop":' + thisStop.to_json(), stops]) + '}'
    return HttpResponse(json)

# return format
# {
#     "type": "all" or "departure" or "destination",   # no thisStop if "all"
#     "thisStop":{stop}
#     "stops":[{stop},{stop}]
# }
