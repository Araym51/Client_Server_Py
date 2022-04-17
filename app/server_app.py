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
    #
    try:
        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])  # получаем параметры, на каком порте запускать сервер
        else:
            server_port = SERVER_PORT
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        print('Не указан номер порта после параметра -р')
        sys.exit(1)
    except ValueError:
        print('Номер порта должен быть в интервале от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            server_ip = sys.argv[sys.argv.index('-a') + 1]  # получаем ip адрес сервера
        else:
            server_ip = SERVER_IP
    except IndexError:
        print('После параметра -а неободимо указать ip адрес')
        sys.exit(1)

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
