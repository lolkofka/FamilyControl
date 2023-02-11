import requests

class device:
    def __init__(self, deviceId = None, device = None, authKey = None):
        self.deviceId = deviceId
        self.authKey = authKey
        self.device = device
    

    def get_device(self, name = None, deviceId = None):
        url = 'https://api.iot.yandex.net/v1.0/user/info'
        headers = {'Authorization':f'Bearer {self.authKey}'}
        r = requests.get(url, headers=headers)
        resp = r.json()
        for device in resp['devices']:
            if device['name'] == name or device['id'] == deviceId:
                self.deviceId = device.get('id')
                self.device = device
                return device
    
    def get_status(self):
        url = 'https://api.iot.yandex.net/v1.0/user/info'
        headers = {'Authorization':f'Bearer {self.authKey}'}
        r = requests.get(url, headers=headers)
        resp = r.json()
        for device in resp['devices']:
            if device['id'] == self.deviceId:
                self.deviceId = device.get('id')
                self.device = device
                return device['capabilities'][0]['state']['value']
    

    def set_state(self, state = False):
        url = 'https://api.iot.yandex.net/v1.0/devices/actions'
        params = {
        	'devices':[{
        		'id': self.deviceId,
        		'actions': [{
        			'type': 'devices.capabilities.on_off',
        			'state': {
        				"instance": "on",
        				'value':state,
        			}
        		}]
        	}]}
        headers = {'Authorization':f'Bearer {self.authKey}'}
        r = requests.post(url, json=params, headers=headers)
        resp = r.json()
        return resp['status'] == 'ok'
        