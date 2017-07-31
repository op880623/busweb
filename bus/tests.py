from django.test import TestCase

from bus.models import BusRoute, BusStop, StopOnRoute


class TestBusRoute(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.r01 = BusRoute(uid='01',name='r01')
        cls.r01.save()
        cls.r02 = BusRoute(uid='02',name='r02')
        cls.r02.save()
        cls.r03 = BusRoute(uid='03',name='r03')
        cls.r03.save()


        cls.s01 = BusStop(uid='01', name='s01')
        cls.s01.save()
        cls.s02 = BusStop(uid='02', name='s02')
        cls.s02.save()
        cls.s03 = BusStop(uid='03', name='s03')
        cls.s03.save()
        cls.s04 = BusStop(uid='04', name='s04')
        cls.s04.save()
        cls.s05 = BusStop(uid='05', name='s05')
        cls.s05.save()
        cls.s06 = BusStop(uid='06', name='s06')
        cls.s06.save()
        cls.s07 = BusStop(uid='07', name='s07')
        cls.s07.save()
        cls.s08 = BusStop(uid='08', name='s08')
        cls.s08.save()
        cls.s09 = BusStop(uid='09', name='s09')
        cls.s09.save()
        cls.s10 = BusStop(uid='10', name='s10')
        cls.s10.save()
        cls.s11 = BusStop(uid='11', name='s11')
        cls.s11.save()
        cls.s12 = BusStop(uid='12', name='s12')
        cls.s12.save()


        cls.q = StopOnRoute(route=cls.r01,stop=cls.s01,direction=True,order=1)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r01,stop=cls.s02,direction=True,order=2)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r01,stop=cls.s03,direction=True,order=3)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r01,stop=cls.s04,direction=True,order=4)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r01,stop=cls.s05,direction=False,order=1)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r01,stop=cls.s06,direction=False,order=2)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r01,stop=cls.s11,direction=False,order=3)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r01,stop=cls.s12,direction=False,order=4)
        cls.q.save()

        cls.q = StopOnRoute(route=cls.r02,stop=cls.s01,direction=True,order=1)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r02,stop=cls.s02,direction=True,order=2)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r02,stop=cls.s07,direction=True,order=3)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r02,stop=cls.s08,direction=True,order=4)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r02,stop=cls.s09,direction=False,order=1)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r02,stop=cls.s10,direction=False,order=2)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r02,stop=cls.s11,direction=False,order=3)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r02,stop=cls.s12,direction=False,order=4)
        cls.q.save()

        cls.q = StopOnRoute(route=cls.r03,stop=cls.s09,direction=True,order=1)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r03,stop=cls.s10,direction=True,order=2)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r03,stop=cls.s03,direction=True,order=3)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r03,stop=cls.s04,direction=True,order=4)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r03,stop=cls.s05,direction=False,order=1)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r03,stop=cls.s06,direction=False,order=2)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r03,stop=cls.s07,direction=False,order=3)
        cls.q.save()
        cls.q = StopOnRoute(route=cls.r03,stop=cls.s08,direction=False,order=4)
        cls.q.save()


class TestBusRouteBasic(TestBusRoute):

    def test_setup_name_and_uid(self):
        self.assertEqual(self.r01.uid, '01')
        self.assertEqual(self.r01.name, 'r01')
        self.assertEqual(self.r02.uid, '02')
        self.assertEqual(self.r02.name, 'r02')
        self.assertEqual(self.r03.uid, '03')
        self.assertEqual(self.r03.name, 'r03')
        self.assertEqual(self.s01.uid, '01')
        self.assertEqual(self.s01.name, 's01')
        self.assertEqual(self.s02.uid, '02')
        self.assertEqual(self.s02.name, 's02')
        self.assertEqual(self.s03.uid, '03')
        self.assertEqual(self.s03.name, 's03')
        self.assertEqual(self.s04.uid, '04')
        self.assertEqual(self.s04.name, 's04')
        self.assertEqual(self.s05.uid, '05')
        self.assertEqual(self.s05.name, 's05')
        self.assertEqual(self.s06.uid, '06')
        self.assertEqual(self.s06.name, 's06')
        self.assertEqual(self.s07.uid, '07')
        self.assertEqual(self.s07.name, 's07')
        self.assertEqual(self.s08.uid, '08')
        self.assertEqual(self.s08.name, 's08')
        self.assertEqual(self.s09.uid, '09')
        self.assertEqual(self.s09.name, 's09')
        self.assertEqual(self.s10.uid, '10')
        self.assertEqual(self.s10.name, 's10')
        self.assertEqual(self.s11.uid, '11')
        self.assertEqual(self.s11.name, 's11')
        self.assertEqual(self.s12.uid, '12')
        self.assertEqual(self.s12.name, 's12')

    def test_route_stops(self):
        ans = []
        for stop in self.r01.stops.filter(stoponroute__direction=True).order_by('stoponroute__order'):
            ans.append(stop.name)
        self.assertEqual('-'.join(ans), 's01-s02-s03-s04')

        ans = []
        for stop in self.r01.stops.filter(stoponroute__direction=False).order_by('stoponroute__order'):
            ans.append(stop.name)
        self.assertEqual('-'.join(ans), 's05-s06-s11-s12')

        ans = []
        for stop in self.r02.stops.filter(stoponroute__direction=True).order_by('stoponroute__order'):
            ans.append(stop.name)
        self.assertEqual('-'.join(ans), 's01-s02-s07-s08')

        ans = []
        for stop in self.r02.stops.filter(stoponroute__direction=False).order_by('stoponroute__order'):
            ans.append(stop.name)
        self.assertEqual('-'.join(ans), 's09-s10-s11-s12')

        ans = []
        for stop in self.r03.stops.filter(stoponroute__direction=True).order_by('stoponroute__order'):
            ans.append(stop.name)
        self.assertEqual('-'.join(ans), 's09-s10-s03-s04')

        ans = []
        for stop in self.r03.stops.filter(stoponroute__direction=False).order_by('stoponroute__order'):
            ans.append(stop.name)
        self.assertEqual('-'.join(ans), 's05-s06-s07-s08')


class TestBusRouteStopsAfterSpecificStop(TestBusRoute):

    def test_with_stop_input(self):
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s01)]), 's02-s03-s04')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s02)]), 's03-s04')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s03)]), 's04')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s04)]), '')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s05)]), 's06-s11-s12')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s06)]), 's11-s12')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s11)]), 's12')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s12)]), '')

    def test_with_stop_id_input(self):
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s01.uid)]), 's02-s03-s04')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s02.uid)]), 's03-s04')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s03.uid)]), 's04')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s04.uid)]), '')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s05.uid)]), 's06-s11-s12')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s06.uid)]), 's11-s12')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s11.uid)]), 's12')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s12.uid)]), '')

    def test_with_stop_name_input(self):
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s01.name)]), 's02-s03-s04')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s02.name)]), 's03-s04')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s03.name)]), 's04')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s04.name)]), '')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s05.name)]), 's06-s11-s12')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s06.name)]), 's11-s12')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s11.name)]), 's12')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_after_specific_stop(self.s12.name)]), '')

    def test_with_error_input(self):
        # test with wrong uid or name
        with self.assertRaisesRegex(ValueError, "BusStop matching this uid or name does not exist."):
            self.r01.stops_after_specific_stop('s00')
        # test with wrong input type
        with self.assertRaisesRegex(TypeError, 'must be a BusStop object or string of BusStop.uid but ' + str(type(1))):
            self.r01.stops_after_specific_stop(1)
        # test with BusStop does not exist
        with self.assertRaisesRegex(NameError, 'is not defined'):
            self.r01.stops_after_specific_stop(s13)
        # test with StopOnRoute does not exist
        with self.assertRaisesRegex(ValueError, "StopOnRoute matching this uid or name does not exist."):
            self.r01.stops_after_specific_stop(self.s07)


class TestBusRouteStopsBeforeSpecificStop(TestBusRoute):

    def test_with_stop_input(self):
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s01)]), '')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s02)]), 's01')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s03)]), 's01-s02')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s04)]), 's01-s02-s03')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s05)]), '')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s06)]), 's05')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s11)]), 's05-s06')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s12)]), 's05-s06-s11')

    def test_with_stop_id_input(self):
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s01.uid)]), '')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s02.uid)]), 's01')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s03.uid)]), 's01-s02')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s04.uid)]), 's01-s02-s03')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s05.uid)]), '')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s06.uid)]), 's05')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s11.uid)]), 's05-s06')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s12.uid)]), 's05-s06-s11')

    def test_with_stop_name_input(self):
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s01.name)]), '')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s02.name)]), 's01')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s03.name)]), 's01-s02')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s04.name)]), 's01-s02-s03')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s05.name)]), '')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s06.name)]), 's05')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s11.name)]), 's05-s06')
        self.assertEqual('-'.join([stop.name for stop in self.r01.stops_before_specific_stop(self.s12.name)]), 's05-s06-s11')

    def test_with_error_input(self):
        # test with wrong uid or name
        with self.assertRaisesRegex(ValueError, "BusStop matching this uid or name does not exist."):
            self.r01.stops_before_specific_stop('s00')
        # test with wrong input type
        with self.assertRaisesRegex(TypeError, 'must be a BusStop object or string of BusStop.uid but ' + str(type(1))):
            self.r01.stops_before_specific_stop(1)
        # test with BusStop does not exist
        with self.assertRaisesRegex(NameError, 'is not defined'):
            self.r01.stops_before_specific_stop(s13)
        # test with StopOnRoute does not exist
        with self.assertRaisesRegex(ValueError, "StopOnRoute matching this uid or name does not exist."):
            self.r01.stops_before_specific_stop(self.s07)
