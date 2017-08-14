import re
from datetime import datetime

from bus.update import *


log('start update route time: ' + datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

with open('bus/routeid.txt', encoding='utf8') as sourceFile:
    idSource = sourceFile.read()

routeIds = re.findall("id: (\S+)", idSource)

for routeId in routeIds:
    update_route(routeId)

log('finish update route time: ' + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + '\n')
