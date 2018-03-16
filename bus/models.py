import re
import json
from time import sleep
from datetime import timedelta

import requests

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class Stop(models.Model):
    uid = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    latitude = models.FloatField(max_length=10, blank=True, null=True)
    longitude = models.FloatField(max_length=10, blank=True, null=True)
    updateDate = models.DateTimeField()

    def __str__(self):
        return self.name

    @classmethod
    def get(cls, uid):
        if cls.objects.filter(uid = uid).exists():
            return cls.objects.get(uid = uid)
        stop = cls(uid = uid)
        stop.updateDate = timezone.now() + timedelta(days=-7)
        stop.update()
        print('create stop %s' % stop.name)
        return stop

    def url(self):
        return "https://ebus.gov.taipei/Stop/RoutesOfStop?stopid=" + self.uid

    def busses(self):
        return Bus.objects.filter(stopsId__contains=[self.uid])

    def update(self):
        info = request_info(self.url())
        if not info:
            return None
        # update name
        name = str(info['Name'])
        if self.name != name:
            print('update - %s name - %s to %s' % (self.uid, self.name, name))
            self.name = name
        # update latitude
        latitude = str(info['Latitude'])
        if self.latitude != latitude:
            print('update - %s %s - latitude' % (self.uid, self.name))
            self.latitude = latitude
        # update longitude
        longitude = str(info['Longitude'])
        if self.longitude != longitude:
            print('update - %s %s - longitude' % (self.uid, self.name))
            self.longitude = longitude
        # save
        self.save()

    def update_bus(self):
        info = request_info(self.url())
        if not info:
            return None
        # update bus of stop
        for bus in info['RoutesNumber']:
            uid = bus['UniRouteId']
            if re.match('\d{9}0', uid):
                Bus.get(uid)
        # save
        self.updateDate = timezone.now()
        self.save()

class Bus(models.Model):
    uid = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    stopsId = ArrayField(models.CharField(max_length=15), blank=True, null=True)
    updateDate = models.DateTimeField()

    def __str__(self):
        return self.name

    @classmethod
    def get(cls, uid):
        if cls.objects.filter(uid = uid).exists():
            return cls.objects.get(uid = uid)
        bus = cls(uid = uid)
        bus.updateDate = timezone.now() + timedelta(days=-7)
        bus.update()
        print('create bus %s' % bus.name)
        return bus

    def url(self):
        return "https://ebus.gov.taipei/Route/StopsOfRoute?routeid=" + self.uid

    def stops(self):
        stopsList = []
        for uid in self.stopsId:
            stopsList.append(Stop.get(uid))
        return stopsList

    def update(self):
        info = request_info(self.url())
        if not info:
            return None
        # update name
        name = str(info['Name'])
        if self.name != name:
            print('update - %s name - %s to %s' % (self.uid, self.name, name))
            self.name = name
        # save
        self.save()

    def update_stop(self):
        info = request_info(self.url())
        if not info:
            return None
        # get data
        stopsData = []
        if isinstance(info['GoDirStops'], list):
            stopsData += info['GoDirStops']
        if isinstance(info['BackDirStops'], list):
            stopsData += info['GoDirStops']
        # make list
        stopsList = []
        for stop in stopsData:
            uid = stop['UniStopId']
            if re.match('\d{9}0', uid):
                stopsList.append(uid)
                Stop.get(uid)
        # update stopsId
        if self.stopsId != stopsList:
            print('update - %s %s - stopsId' % (self.uid, self.name))
            self.stopsId = stopsList
        # save
        self.updateDate = timezone.now()
        self.save()

def request_info(url):
    page = requests.get(url)
    sleep(0.5)
    if page.status_code != 200:
        # it's usually 404 page
        print('warning - website ' + url + ' is broken or not found.')
        return None
    try:
        jsonTxt = re.search('= JSON\.stringify\((.+)\);', page.text).group(1)
    except:
        # a url redirect to other page cause this
        print('warning - info of ' + url + ' can\'t be extracted.')
        return None
    return json.loads(jsonTxt)
