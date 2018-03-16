from django.shortcuts import render
from django.http import HttpResponse


def all_stops(request):
    json = ''
    return HttpResponse(json)

def departure(request, uid):
    json = ''
    return HttpResponse(json)

def destination(request, uid):
    json = ''
    return HttpResponse(json)

def connected(request, uid):
    json = ''
    return HttpResponse(json)
