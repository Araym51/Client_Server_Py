import socket
import sys
import json
import select
import time
from common.constants import *
from common.utils import send_message, recieve_message
import logging
import loging.server_conf_log
from errors import IncorrectDataRecievedError
from logging_deco import log

SERVER_LOGGER = logging.getLogger('server')

@log
def process_client_message(message):
    """
    функция для проверки корректности входящих данных от клиентов
    :param message:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщение от клиента: {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'bad request'
    }


def main():
    #
    try:
        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])  # получаем параметры, на каком порте запускать сервер
        else:
            server_port = SERVER_PORT
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.critical('Попытка запуска с заданными параметрами без '
                               'указания номера портаа после параметра -р')
        # print('Не указан номер порта после параметра -р')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical('Запуск сервера с неверным параметром номера порта'
                               'Номер порта должен быть в интервале от 1024 до 65535')
        # print('Номер порта должен быть в интервале от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            server_ip = sys.argv[sys.argv.index('-a') + 1]  # получаем ip адрес сервера
        else:
            server_ip = SERVER_IP
    except IndexError:
        print('После параметра -а неободимо указать ip адрес')
        sys.exit(1)

    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {server_port}, '
                       f'ip: {server_ip}')
    # готовим сокет
    SERV_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # оствобождаем порт:
    SERV_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # назначаем параметры сокета из констант:
    SERV_SOCKET.bind((server_ip, server_port))

    # таймаут
    SERV_SOCKET.settimeout(0.5)
    # список клиентов
    clients_list = []
    # очередь сообщений
    message_list = []

    # слушаем порт
    SERV_SOCKET.listen(MAX_CONNECTIONS)

    # запускаем сервер:
    while True:
        try:
            #пытаемся соединится с клиентом:
            client, client_adress = SERV_SOCKET.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соединение с {client_adress}')
            clients_list.append(client) # закончил тут, продолжить дальше


if __name__ == '__main__':
    main()
