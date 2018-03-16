from datetime import timedelta

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from bus.models import Bus, Stop

class Command(BaseCommand):
    help = "Update bus stop relationship"

    def add_arguments(self, parser):
        parser.add_argument('continue', nargs = '?', default = 0, type = float)

    def handle(self, *args, **options):
        # determine standard
        if options['continue']:
            standard = timezone.now() + timedelta(hours=-options['continue'])
        else:
            standard = timezone.now() + timedelta(days=-7)

        # update bus of stop
        print('start update bus of stop')
        for stop in Stop.objects.all():
            if stop.updateDate < standard:
                print('update stop %s' % stop.uid)
                stop.update_bus()
            else:
                print('skip update stop %s' % stop.uid)

        # update stop of bus
        print('start update stop of bus')
        for bus in Bus.objects.all():
            if bus.updateDate < standard:
                print('update bus %s' % bus.uid)
                bus.update_stop()
            else:
                print('skip update bus %s' % bus.uid)

        print('update finish.')
