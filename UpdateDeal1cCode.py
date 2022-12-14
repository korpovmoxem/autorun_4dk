from fast_bitrix24 import Bitrix
import requests
from tools import *

from authentication import authentication



webhook = authentication('Bitrix')
b = Bitrix(webhook)



def update_deal_1c_code():
    success_count = 0
    deals = b.get_all('crm.deal.list', {
        'select': ['*', 'UF_*'],
        'filter': {
            'CATEGORY_ID': '1',
            'UF_CRM_1657878818384': [  # Группа
                '859',  # ИТС
                '907',  # Сервисы ИТС
            ],
            'STAGE_ID': [
                'C1:NEW',  # Услуга активна
                'C1:UC_0KJKTY',  # Счет сформирован
                'C1:UC_3J0IH6',  # Счет отправлен клиенту
                'C1:UC_KZSOR2',  # Нет оплаты
                'C1:UC_VQ5HJD',  # Ждём решения клиента
            ]
        }})
    deals = list(filter(lambda x: x['UF_CRM_1655972832'] in [None, 'None'], deals))
    count = 0
    error_text = ''
    for deal in deals:
        count += 1
        print(f'{count} | {len(deals)}')

        try:
            deal_id = deal['ID']

            # Получение информации о продукте сделки

            deal_product = requests.get(url=webhook + 'crm.deal.productrows.get.json?id=' + deal_id)

            # ID продукта сделки

            id_deal_product = str(deal_product.json()['result'][0]['PRODUCT_ID'])


            # Получение полей продукта

            product_fields = requests.get(url=webhook + 'crm.product.get.json?id=' + id_deal_product)

            # Получение кода 1С

            if product_fields.json()['result']['PROPERTY_139'] is None:
                error_text += f"{deal_id}\n"
            code_1c = product_fields.json()['result']['PROPERTY_139']['value']

            # Сверка кода 1С продукта и кода в сделке

            deal_1c_code = requests.get(url=f"{webhook}crm.deal.get?id={deal_id}").json()['result']['UF_CRM_1655972832']

            if deal_1c_code != code_1c:

                # Запись кода в сделку

                requests.post(url=f"{webhook}crm.deal.update?id={deal_id}&fields[UF_CRM_1655972832]={code_1c}")

                success_count += 1
        except:
            error_text += f"{deal_id}\n"

    data = {
        'USER_ID': '1',
        'MESSAGE': f'Поле "СлужКод1С было обновлено в {success_count} сделках'
    }
    send_bitrix_request('im.notify.system.add', data)

if __name__ == '__main__':
    update_deal_1c_code()
