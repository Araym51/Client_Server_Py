import socket
import sys
import json
from common.constants import *
from common.utils import send_message, recieve_message


def process_client_message(message):
    """
    функция для проверки корректности входящих данных от клиентов
    :param message:
    :return:
    """
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'bad request'
    }


def main():
    # готовим сокет
    SERV_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # оствобождаем порт:
    SERV_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # назначаем параметры сокета из констант:
    SERV_SOCKET.bind((SERVER_IP, SERVER_PORT))

    # слушаем порт
    SERV_SOCKET.bind(MAX_CONNECTIONS)

    # запускаем сервер:
    while True:
        client, client_adress = SERV_SOCKET.accept()
        try:
            message_from_client = recieve_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Что-то пошло не по плану')
            client.close()


if __name__ == '__main__':
    main()