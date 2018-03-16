import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from django.core.management.base import BaseCommand, CommandError

from bus.models import Bus

class Command(BaseCommand):
    help = "Find busses"

    def handle(self, *args, **options):
        print('collecting busses...')
        browser = webdriver.PhantomJS()
        browser.get('https://ebus.gov.taipei/Query/BusRoute')
        uids = set()
        but_clear = browser.find_element_by_css_selector(".findroute-mainboard-li-clear")
        for but in browser.find_elements_by_css_selector('ul.findroute-mainboard-ul>li'):
            ActionChains(browser).click(but).click(but_clear).perform()
            sleep(5)
            new_uids = re.findall('routeid=([\d\w]{10})', browser.page_source)
            uids = uids.union(set(new_uids))
        browser.quit()
        for uid in uids:
            Bus.get(uid)
        print('complete collecting busses.')
