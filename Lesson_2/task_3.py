"""
3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных
в файле YAML-формата.Для этого:

Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,в файл file.yaml. При этом обеспечить стилизацию файла
с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""

import yaml

dict_to_yaml = {
    'list': [1, 'one'],
    'int': 123,
    'dict': {
        'price': '1000 €',
        'price_2': '100 $'
    }
}

with open('file.yaml', 'w', encoding='utf-8') as yaml_file:
    yaml.dump(dict_to_yaml, yaml_file, default_flow_style=True, allow_unicode=True)

with open('file.yaml', 'r', encoding='utf-8') as file:
    dict_from_yaml = yaml.load(file, Loader=yaml.SafeLoader)
    print(file.read()) # результат команды print: {dict: {price: 1000 €, price_2: 100 $}, int: 123, list: [1, one]}

print(dict_from_yaml == dict_to_yaml)
