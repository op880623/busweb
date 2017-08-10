from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse

from .models import BusStop, BusRoute


def all_atops(request):
    stops = get_list_or_404(BusStop)
    json = '{"response_type":"all","stops":[' + ','.join([stop.to_json() for stop in stops]) + ']}'
    return HttpResponse(json)


def departure(request, uid):
    thisStop = get_object_or_404(BusStop, uid=uid)
    response_type = '"response_type":"departure"'
    stops = '"stops":[' + ','.join([stop['stop'].to_json() for stop in thisStop.stops_can_go()]) + ']'
    json = '{' + ','.join([response_type, '"thisStop":' + thisStop.to_json(), stops]) + '}'
    return HttpResponse(json)


def destination(request, uid):
    thisStop = get_object_or_404(BusStop, uid=uid)
    response_type = '"response_type":"destination"'
    stops = '"stops":[' + ','.join([stop['stop'].to_json() for stop in thisStop.stops_can_come()]) + ']'
    json = '{' + ','.join([response_type, '"thisStop":' + thisStop.to_json(), stops]) + '}'
    return HttpResponse(json)

# return format
# {
#     "response_type": "all" or "departure" or "destination",   # no thisStop if "all"
#     "thisStop":{stop}
#     "stops":[{stop},{stop}]
# }
