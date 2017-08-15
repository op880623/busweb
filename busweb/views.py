from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse

from bus.models import BusStop, BusRoute


def map(request):
    return render(request, 'map.html')
