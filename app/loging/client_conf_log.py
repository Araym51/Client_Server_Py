import sys
import os
import logging
from app.common.constants import LOGGING_LEVEL
sys.path.append('..')


# задаём форму вывода для логов:
CLIENT_LOG_FORMAT = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# задаём файл для логов
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'clien.log')

# потоки вывода логов
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
# Задаём формат
STREAM_HANDLER.setFormatter(CLIENT_LOG_FORMAT)
STREAM_HANDLER.setLevel(logging.ERROR)
#устанавливаем кодировку
LOG_FILE = logging.FileHandler(PATH, encoding='utf-8')
LOG_FILE.setFormatter(CLIENT_LOG_FORMAT)

#настройки регистратора
CLIENT_LOGGER = logging.getLogger('client')
CLIENT_LOGGER.addHandler(STREAM_HANDLER)
CLIENT_LOGGER.addHandler(LOG_FILE)
CLIENT_LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    CLIENT_LOGGER.critical('Критическая ошибка')
    CLIENT_LOGGER.error('Ошибка')
    CLIENT_LOGGER.debug('Отладочная информация')
    CLIENT_LOGGER.info('Информационное сообщение')