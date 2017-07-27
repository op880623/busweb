from django.db import models


class BusStop(models.Model):
    uid = models.CharField(max_length=15)# id used in target website
    name = models.CharField(max_length=100)
    route = models.ManyToManyField('BusRoute', through='StopOnRoute')
    latitude = models.FloatField(max_length=10, blank=True, null=True)
    longitude = models.FloatField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class BusRoute(models.Model):
    uid = models.CharField(max_length=15)# id used in target website
    name = models.CharField(max_length=100)
    stops = models.ManyToManyField(BusStop, through='StopOnRoute')

    def __str__(self):
        return self.name

class StopOnRoute(models.Model):
    route = models.ForeignKey(BusRoute, blank=True, null=True)
    stop = models.ForeignKey(BusStop, blank=True, null=True)
    direction = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.route.name + '-' + self.stop.name
