import argparse
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
def process_client_message(message, messages_list, client):
    """
    функция для проверки корректности входящих данных от клиентов
    :param message:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщение от клиента: {message}')
    # если клиент сообщает о присутствии, подтверждаем, что видим его
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and message[USER][
        ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    # Если это сообщение, добавляем его в список сообщений
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


def args_reader():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=SERVER_PORT, type=int, nargs='?')
    parser.add_argument('-a', default=SERVER_IP, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    serv_adress = namespace.a
    serv_port = namespace.p

    if not 1023 < serv_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{serv_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return serv_adress, serv_port


def main():
    #
    server_ip, server_port = args_reader()

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
            # пытаемся соединится с клиентом:
            client, client_adress = SERV_SOCKET.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соединение с {client_adress}')
            clients_list.append(client)  # закончил тут, продолжить дальше

        recived_data = []
        send_data = []
        errors_lst = []
        # проверяем наличие клиентов:
        try:
            if clients_list:
                recived_data, send_data, errors_lst = select.select(clients_list, clients_list, [], 0)
        except OSError:
            pass

        if recived_data:
            for client_with_message in recived_data:
                try:
                    process_client_message(recieve_message(client_with_message), message_list, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} отключился')
                    clients_list.remove(client_with_message)

        if message_list in send_data:
            message = {
                ACTION: MESSAGE,
                SENDER: message_list[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: message_list[0][1]
            }
            del message_list[0]
            for waiting_client in send_data:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'лиент {waiting_client.getpeername()} отключился от сервера')
                    clients_list.remove(waiting_client)


if __name__ == '__main__':
    main()
