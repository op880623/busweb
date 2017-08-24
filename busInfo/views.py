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
            stop = stopData[stopId]
            stops.append('"' + stop.uid + '":' + stop.to_json())
    json = '{' + ','.join(stops) + '}'
    return HttpResponse(json)


def departure(request, uid):
    with shelve.open(dbStop) as stopData:
        thisStop = stopData[uid]
    stops = ['"' + stop + '"'for stop in thisStop.stops_can_go(dbRoute=dbRoute)]
    json = '{"stops":[' + ','.join(stops) + ']}'
    return HttpResponse(json)


def destination(request, uid):
    with shelve.open(dbStop) as stopData:
        thisStop = stopData[uid]
    stops = ['"' + stop + '"'for stop in thisStop.stops_can_come(dbRoute=dbRoute)]
    json = '{"stops":[' + ','.join(stops) + ']}'
    return HttpResponse(json)

# return format
# {
#     "type": "all" or "departure" or "destination",   # no thisStop if "all"
#     "thisStop":{stop}
#     "stops":[{stop},{stop}]
# }
