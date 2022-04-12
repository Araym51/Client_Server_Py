"""
2. Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись
данных в виде словаря в файл orders.json. При записи данных указать
величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.

ПРОШУ ВАС НЕ УДАЛЯТЬ ИСХОДНЫЙ JSON-ФАЙЛ
ПРИМЕР ТОГО, ЧТО ДОЛЖНО ПОЛУЧИТЬСЯ

{
    "orders": [
        {
            "item": "принтер", (возможные проблемы с кирилицей)
            "quantity": "10",
            "price": "6700",
            "buyer": "Ivanov I.I.",
            "date": "24.09.2017"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        }
    ]
}

вам нужно подгрузить JSON-объект
и достучаться до списка, который и нужно пополнять
а потом сохранять все в файл
"""

import json
from pathlib import Path

dict_to_json = {
    'item': 'ASUS ROG STRIX G17 G713IM-HX017W',
    'quantity': 1,
    'price': 169280,
    'buyer': 'Egorka',
    'date': '10.04.2022'
}


def write_order_to_json(record_data, indent):
    """
    Принимает словарь, записывает его в "orders"
    :param record_data: словарь, который необходимо записать
    :param indent: отступ
    :return: json файл с заполненым словарем order
    """
    path = Path('orders.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    data["orders"].append(record_data)
    path.write_text(json.dumps(data, sort_keys=True, indent=indent), encoding='utf-8')

write_order_to_json(dict_to_json, 4)
