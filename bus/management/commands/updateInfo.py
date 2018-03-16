from django.core.management.base import BaseCommand, CommandError

from bus.models import Bus, Stop

class Command(BaseCommand):
    help = "Update bus stop infomation"

    def handle(self, *args, **options):
        for stop in Stop.objects.all():
            stop.update()
        for bus in Bus.objects.all():
            bus.update()
        print('update finish.')
