import logging
import sys
import json
import socket
import time
from common.constants import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, SERVER_PORT, SERVER_IP
from common.utils import recieve_message, send_message
import logging
import loging.client_conf_log
from errors import ReqFieldMissingError
from logging_deco import log

CLIENT_LOGGER = logging.getLogger('client')

@log
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
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для {account_name}')
    # print(f'Сформировано {PRESENCE} сообщение для {account_name}')
    return presence_message

@log
def process_answer(message):
    """
    функция разбирает ответ сервера
    :param message:
    :return:
    """
    CLIENT_LOGGER.debug(f'расшифровка сообщения от сервера: {message}')
    # print(f'расшифровка сообщения от сервера: {message}')
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
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с недопустимым параметром номера порта {server_port}'
            f'Допустимые порты с 1024 по 65535. Клиент завершает работу'
        )
        # print('Порт необходимо указать в диапазоне от 1024 до 65535')

    CLIENT_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT_SOCK.connect((server_adress, server_port))
    presence_message = create_presence()
    send_message(CLIENT_SOCK, presence_message)
    CLIENT_LOGGER.debug(f'клиент запущен с параметрами {server_adress} : {server_port}')
    # print(f'клиент запущен с параметрами {server_adress} : {server_port}')
    try:
        answer = process_answer(recieve_message(CLIENT_SOCK))
        CLIENT_LOGGER.info(f'принят ответ от сервера {answer}')
        # print(answer)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Ошибка обработки JSON строки')
        # print('Не удалось декодировать сообщение')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_adress}:{server_port},'
                               f'запрос на подключение отвергнут')
    except ReqFieldMissingError as field:
        CLIENT_LOGGER.error(f'В принятом словаре отсутствует необходимое поле:'
                            f'{field.missing_field}')

if __name__ == '__main__':
    main()
