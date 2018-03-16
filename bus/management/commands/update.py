import requests
from selenium import webdriver

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from bus.models import Bus, Stop

class Command(BaseCommand):
    help = "Update bus stop"

    def handle(self, *args, **options):
        print('update finish.')
