from requests import request
from fast_bitrix24 import Bitrix
from authentication import authentication

r = request(method='GET', url='http://141.8.194.146:5000')

if r.status_code != 200:
    with open('/root/autorun_4dk/status_web_app.txt', 'r') as file:
        status = file.read().split(': ')[-1]
    if status == 'online':
        with open('/root/autorun_4dk/status_web_app.txt', 'w') as file:
            file.write('Status_web_app: offline')

        b = Bitrix(authentication('Bitrix'))
        b.call('tasks.task.add', {
            'fields': {
                'RESPONSIBLE_ID': '311',
                'ACCOMPLICES': '1',
                'GROUP_ID': '13',
                'TITLE': 'Работа веб-приложения остановлена',
            }
        })
else:
    with open('/root/autorun_4dk/status_web_app.txt', 'r') as file:
        status = file.read().split(': ')[-1]
    if status == 'offline':
        with open('/root/autorun_4dk/status_web_app.txt', 'w') as file:
            file.write('Status_web_app: online')
