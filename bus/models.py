from django.db import models
from django.contrib.postgres.fields import ArrayField


class Stop(models.Model):
    uid = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    latitude = models.FloatField(max_length=10, blank=True, null=True)
    longitude = models.FloatField(max_length=10, blank=True, null=True)
    # busses = models.ManyToManyField('Bus', through='BusStop')

    def __str__(self):
        return self.name

class Bus(models.Model):
    uid = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    # stops = models.ManyToManyField(Stop, through='BusStop')
    stops = ArrayField(models.CharField(max_length=15), blank=True, null=True)

    def __str__(self):
        return self.name
