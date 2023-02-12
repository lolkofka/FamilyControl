import configparser

config = configparser.ConfigParser()
config.read("settings.ini", encoding='utf-8')

#YandexSmart
authKey = config['YandexSmart']['YandexAuthKey']
deviceName = config['YandexSmart']['deviceName']

#settings
timeToPlay = int(config['ScriptSettings']['timeToPlay'])
resetTime = config['ScriptSettings']['resetTime']

#telegram
tgToken = config['TelegramBot']['tgToken']
parentsIds = eval(config['TelegramBot']['parentsIds'])
childs = eval(config['TelegramBot']['childs'])