import argparse
import logging
import sys
import json
import socket
import time
from common.constants import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, SERVER_PORT, SERVER_IP, \
    MESSAGE, SENDER, MESSAGE_TEXT
from common.utils import recieve_message, send_message
import logging
import loging.client_conf_log
from errors import ReqFieldMissingError, ServerError
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
        elif message[RESPONSE] == 400:
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=SERVER_IP, nargs='?')
    parser.add_argument('port', default=SERVER_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_ip = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
                               f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'запуск в недопустимом режиме работы {client_mode},'
                               f'допустимые режимы: listen, send')
        sys.exit(1)

    return server_ip, server_port, client_mode


@log
def message_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and SENDER in MESSAGE in message and MESSAGE_TEXT in message:
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя'
                           f'{message[SENDER]}: \n {message[MESSAGE_TEXT]}')
        print(f'Получено сообщение от пользователя'
              f'{message[SENDER]}: \n {message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получен некорректный ответ от сервера {message}')


@log
def create_message(sock, account_name='Guest'):
    message = input('Введите сообщение для отправки или \" !!! \" для закрытия программы')
    if message == '!!!':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде пользователя')
        print('Выход из программы. Возвращайтесь!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформировано сообщение: {message_dict}')
    return message_dict


def main():
    server_adress, server_port, client_mode = arg_parser()

    CLIENT_LOGGER.info(f'Запущен клиент с параметрами: '
                       f'адрес сервера: {server_adress}, '
                       f'порт сервера: {server_port},'
                       f'режим работы: {client_mode}')

    try:
        CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CLIENT.connect((server_adress, server_port))
        send_message(CLIENT, create_presence())
        answer = process_answer(recieve_message(CLIENT))
        CLIENT_LOGGER.info(f'становлено соединение с сервером. Ответ от сервера: {answer}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать json строку')
        sys.exit(1)
    except ServerError as error_ans:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {error_ans.text}')
        sys.exit(1)
    except ReqFieldMissingError as error_mis:
        CLIENT_LOGGER.error(f'тсутствует необходимое поле в ответе от сервера: {error_mis.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_adress}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        if client_mode == 'send':
            print('Готов к отправке сообщений')
        else:
            print('Готов к приему сообщений')
        while True:
            # режим отправки сообщений:
            if client_mode == 'send':
                try:
                    send_message(CLIENT, create_message(CLIENT))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Потеряно соединение с сервером: {server_adress}')
                    sys.exit(1)
            # режим приема сообщений:
            if client_mode == 'listen':
                try:
                    message_from_server(recieve_message(CLIENT))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Потеряно соединение с сервером: {server_adress}')
                    sys.exit(1)



if __name__ == '__main__':
    main()
