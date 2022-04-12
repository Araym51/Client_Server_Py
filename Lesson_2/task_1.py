"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
«отчетный» файл в формате CSV. Для этого:
a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения
каждого параметра поместить в соответствующий список. Должно получиться четыре
списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
функции создать главный список для хранения данных отчета — например, main_data
— и поместить в него названия столбцов отчета в виде списка: «Изготовитель
системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data (также для
каждого файла);
b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
функции реализовать получение данных через вызов функции get_data(), а также
сохранение подготовленных данных в соответствующий CSV-файл;
c. Проверить работу программы через вызов функции write_to_csv().
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
                splited = line.split()
                if splited[0] == 'Название':
                    temp = ' '.join(splited[2:])
                    os_name_list.append(temp)
                if splited[0] == 'Код':
                    temp = ' '.join(splited[2:])
                    os_code_list.append(temp)
                if (splited[0] == 'Изготовитель') and (splited[1] == 'системы:'):
                    temp = ' '.join(splited[2:])
                    os_prod_list.append(temp)
                if splited[0] == 'Тип':
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
    with open('result.csv', 'w') as file:
        file_writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        for row in data_list:
            file_writer.writerow(row)


data = get_data(files)
write_to_csv(data)
