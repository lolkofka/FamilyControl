import additions.config as config
import additions.iot as iot
from additions.database import db

import time


database = db('database.json')
pc = iot.device(authKey=config.authKey)
s = pc.get_device(config.deviceName)

def needOffPc():
    workTime = database.get('workTime')
    if not workTime: return False
    if workTime.get('time') > config.timeToPlay: return True

while True:
    pcStatus = pc.get_status()
    if not pcStatus or needOffPc():
        pc.set_state(False)
    else:
        workTime = database.get('workTime')
        if not workTime: workTime = {'time':0}
        database.set('workTime', {'time':workTime.get('time')+5})
    time.sleep(5)