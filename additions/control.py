import additions.config as config
import additions.iot as iot
from additions.database import db

import time


database = db('database.json')
pc = iot.device(authKey=config.authKey)
pc.get_device(config.deviceName)

def needOffPc():
    workTime = database.get('workTime')
    if not workTime: return False
    if workTime > config.timeToPlay: return True

def startControl(): #Основной цикл
    resetDay = database.get('resetDay')
    if resetDay: 
        if resetDay != (time.time()+3600*3)//86400: # Проверка на сброс времени до этого
            database.set('workTime', 0)
            database.set('resetDay', (time.time()+3600*3)//86400) 
            
    while True: # Запуск бесконечного цикла
        pcStatus = pc.get_status()
        if not pcStatus or needOffPc(): # Проверка на включение компьютера в алисе
            pc.set_state(False) # Запрос на выключение
        else:
            workTime = database.get('workTime')
            if not workTime: workTime = 0
            database.set('workTime', workTime+5) # Добавляем 5 секунд к времени
        hours = time.strftime("%H:%M", time.gmtime((time.time()+3600*3)))
        if hours == config.resetTime:
            database.set('workTime', 0)
            database.set('resetDay', (time.time()+3600*3)//86400) #Сброс времени ночью
        time.sleep(5) #Ожидание 5 секунд