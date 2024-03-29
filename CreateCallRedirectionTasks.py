from datetime import datetime, timedelta

from fast_bitrix24 import Bitrix

from authentication import authentication


b = Bitrix(authentication('Bitrix'))


def create_call_redirection_tasks():
    filter_date = (datetime.now() + timedelta(days=1)).strftime('%d.%m.%Y')
    elements = b.get_all('lists.element.get', {
        'IBLOCK_TYPE_ID': 'lists',
        'IBLOCK_ID': '159',
        'filter': {
            'PROPERTY_1233': filter_date,
        }
    })

    for element in elements:
        user_id = list(element['PROPERTY_1235'].values())[0]
        user_info = b.get_all('user.get', {'id': user_id})[0]
        user_name = f"{user_info['LAST_NAME']} {user_info['NAME']}"
        department_info = b.get_all('department.get', {'ID': user_info['UF_DEPARTMENT'][0]})[0]
        vacation_start = list(element['PROPERTY_1233'].values())[0]
        vacation_end = list(element['PROPERTY_1237'].values())[0]
        b.call('tasks.task.add', {
            'fields': {
                'TITLE': f"Переадресация с {user_name} {vacation_start} - {vacation_end}",
                'DESCRIPTION': f"{user_name} уходит в отпуск с {vacation_start} по {vacation_end}. В связи с этим необходимо настроить переадресацию звонков с этого сотрудника на другого",
                'CREATED_BY': '173',
                'RESPONSIBLE_ID': department_info['UF_HEAD'],
                'ACCOMPLICES': ['133', ],
                'DEADLINE': datetime.now().strftime('%Y-%m-%d 19:00:00'),
            }
        })


if __name__ == '__main__':
    create_call_redirection_tasks()