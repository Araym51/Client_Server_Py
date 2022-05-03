import socket
import sys
import json
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

    # слушаем порт
    SERV_SOCKET.listen(MAX_CONNECTIONS)

    # запускаем сервер:
    while True:
        client, client_adress = SERV_SOCKET.accept()
        SERVER_LOGGER.info(f'установлено соединение с {client_adress}')
        try:
            message_from_client = recieve_message(client)
            SERVER_LOGGER.debug(f'получено сообщение {message_from_client}')
            # print(message_from_client)
            response = process_client_message(message_from_client)
            SERVER_LOGGER.info(f'сформирован ответ клиенту: {response}')
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            SERVER_LOGGER.error(f'Не удалось декодировать JSON строку, полученную от '
                                f'клиента {client_adress}. Соединение закрывается.')
            # print('Что-то пошло не по плану')
            client.close()
        except IncorrectDataRecievedError:
            SERVER_LOGGER.error(f'приняты некорректные данные от {client_adress}.'
                                f'Соединение разорвано')
            client.close()


if __name__ == '__main__':
    main()
