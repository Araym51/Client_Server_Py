"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений или другого инструмента извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""

import csv

files = ['info_1.txt', 'info_2.txt', 'info_3.txt']


def get_data(files):
    """
    функция принимает список фалов, возвращает подготовленный список для записи в csv файл.
    :param files: список файлов для прочтения
    :return: подготовленный список для записи в csv файл
    """
    header = ['Название ОС', 'Код продукта', 'Изготовитель системы', 'Тип системы']
    os_name_list = []
    os_code_list = []
    os_prod_list = []
    os_type_list = []
    main_data = []
    for file in files:
        with open(file, 'r') as data:
            for line in data:
                if line[:8] == 'Название':
                    splited = line.split()
                    temp = ' '.join(splited[2:])
                    os_name_list.append(temp)
                if line[:3] == 'Код':
                    splited = line.split()
                    temp = ' '.join(splited[2:])
                    os_code_list.append(temp)
                if line[:21] == 'Изготовитель системы:':
                    splited = line.split()
                    temp = ' '.join(splited[2:])
                    os_prod_list.append(temp)
                if line[:3] == 'Тип':
                    splited = line.split()
                    temp = ' '.join(splited[2:])
                    os_type_list.append(temp)
    main_data.append(header)
    main_data.append(os_prod_list)
    main_data.append(os_name_list)
    main_data.append(os_code_list)
    main_data.append(os_type_list)
    return main_data


def write_to_csv(data_list):
    """
    функция принимает список, и возвращает .csv файл с результатом
    :param data_list: сюда передавать список со значениями
    :return: возвращает csv файл
    """
    with open('result.csv', 'w', encoding='utf-8') as file:
        file_writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        for row in data_list:
            file_writer.writerow(row)


data = get_data(files)
write_to_csv(data)
