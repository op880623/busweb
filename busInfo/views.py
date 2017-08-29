import shelve

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse

from .models import BusStop, BusRoute


dbRoute = 'busInfo/db/route'
dbStop = 'busInfo/db/stop'


def all_stops(request):
    with shelve.open(dbStop) as stopData:
        stops = ['"' + stopId + '":' + stopData[stopId].to_json()
            for stopId in stopData]
    stop = '"stop":{' + ','.join(stops) + '}'
    with shelve.open(dbRoute) as routeData:
        routes = ['"' + routeId + '":"' + routeData[routeId].name + '"'
            for routeId in routeData]
    route = '"route":{' + ','.join(routes) + '}'
    json = '{' + stop + ',' + route + '}'
    return HttpResponse(json)


def departure(request, uid):
    with shelve.open(dbStop) as stopData:
        thisStop = stopData[uid]
    stops = ['"' + stop + '"'for stop in thisStop.stops_can_go(dbRoute=dbRoute)]
    stopsCanGo = '"departure":[' + ','.join(stops) + ']'
    json = '{' + stopsCanGo + '}'
    return HttpResponse(json)


def destination(request, uid):
    with shelve.open(dbStop) as stopData:
        thisStop = stopData[uid]
    stops = ['"' + stop + '"'for stop in thisStop.stops_can_come(dbRoute=dbRoute)]
    stopsCanCome = '"destination":[' + ','.join(stops) + ']'
    json = '{' + stopsCanCome + '}'
    return HttpResponse(json)


def connected(request, uid):
    with shelve.open(dbStop) as stopData:
        thisStop = stopData[uid]
    stops = ['"' + stop + '"'for stop in thisStop.stops_can_go(dbRoute=dbRoute)]
    stopsCanGo = '"departure":[' + ','.join(stops) + ']'
    stops = ['"' + stop + '"'for stop in thisStop.stops_can_come(dbRoute=dbRoute)]
    stopsCanCome = '"destination":[' + ','.join(stops) + ']'
    json = '{' + stopsCanGo + ',' + stopsCanCome + '}'
    return HttpResponse(json)


# return format
# {
#     "type": "all" or "departure" or "destination",   # no thisStop if "all"
#     "thisStop":{stop}
#     "stops":[{stop},{stop}]
# }
