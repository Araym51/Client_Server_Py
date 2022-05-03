import argparse
import logging
import sys
import json
import socket
import time
from common.constants import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, SERVER_PORT, SERVER_IP, \
    MESSAGE, SENDER, MESSAGE_TEXT, EXIT, DESTINATION
from common.utils import recieve_message, send_message
import logging
import loging.client_conf_log
from errors import ReqFieldMissingError, ServerError, IncorrectDataRecievedError
from logging_deco import log

CLIENT_LOGGER = logging.getLogger('client')


@log
def exit_message(acoount_name):
    """Функция создает сообщение о выходе из программы"""
    CLIENT_LOGGER.info(f'{acoount_name} вышел из программы.')
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: acoount_name
    }


@log
def message_from_server(sock, my_username):
    """функция обработчик сообщений от других пользователей, поступающих с сервера"""
    while True:
        try:
            message = recieve_message(sock)
            if ACTION in MESSAGE and message[
                ACTION] == MESSAGE and SENDER in message and DESTINATION in message and MESSAGE_TEXT in message and \
                    message[DESTINATION] == my_username:
                print(f'\n Получено сообщение от пользователя {message[SENDER]}:'
                      f'\n {message[MESSAGE_TEXT]}')
                CLIENT_LOGGER.info(f'\n Получено сообщение от пользователя {message[SENDER]}:'
                                   f'\n {message[MESSAGE_TEXT]}')
            else:
                CLIENT_LOGGER.error(f'принято некорректное сообщение от сервера {message}')
        except IncorrectDataRecievedError:
            CLIENT_LOGGER.error(f'Не удалось декодировать сообщение')
        except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
            CLIENT_LOGGER.critical(f'потеряно соединение с сервером')
            break


@log
def create_message(sock, acoount_name = 'Guest'):
    """
    Функция запрашивает, кому отправить сообщение, и отправляет полученные данные на срвер
    """
    to_user = input("Введите получателя сообщения: ")
    message = input("Введите сообщение")
    message_dict = {
        ACTION: MESSAGE,
        SENDER: acoount_name,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформировано сообщение: {message_dict}')
    try:
        send_message(sock, message_dict)
        CLIENT_LOGGER.info(f'Отправлено сообщение пользователю {to_user}')
    except:
        CLIENT_LOGGER.critical(f'Потеряно соединение с сервером')
        sys.exit(1)


@log
def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, exit_message(username))
            print('завершение работы')
            CLIENT_LOGGER.info(f'{username} завершил работу')
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


def print_help():
    """Функция выводящяя справку по использованию"""
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@log
def create_presence(account_name='Guest'):
    """
    функция сообщает серверу о присутствии account_name
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

# продолжить со 164 строки
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
