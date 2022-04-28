"""Возможные ошибки"""

class ReqFieldMissingError(Exception):
    """Отсутствует обязательное поле в принятом словаре"""
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В принятом словаре отуствтвует обязательное поле {self.missing_field}'


class IncorrectDataRecievedError(Exception):
    """получение некорректных данных из сокета"""
    def __str__(self):
        return 'Принято некорректное сообщение от клиента'
