
import sys
import json
import socket
import time
from common.constants import *
from common.utils import recieve_message, send_message


def create_presence(account_name='Guest'):
    """
    функция сообщает серверу о присутствии account_name
    :param account_name:
    :return:
    """
    presence_message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return presence_message


def process_answer(message):
    """
    функция разбирает ответ сервера
    :param message:
    :return:
    """
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    try:
        server_adress = sys.argv[2]
        server_port = int(sys.argv[3])
        if server_port < 1024 and server_port > 65535:
            raise ValueError
    except IndexError:
        server_adress = SERVER_IP
        server_port = SERVER_PORT
    except ValueError:
        print('Порт необходимо указать в диапазоне от 1024 до 65535')

    CLIENT_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT_SOCK.connect((server_adress, server_port))
    presence_message = create_presence()
    send_message(CLIENT_SOCK, presence_message)
    try:
        answer = process_answer(recieve_message(CLIENT_SOCK))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение')


if __name__ == '__main__':
    main()
