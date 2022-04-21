import json

from ..common.constants import *
from ..common.utils import send_message, recieve_message
import unittest
from unittest import TestCase, main


class TestSock:
    def __init__(self, test_data):
        self.test_data = test_data
        self.send_message = None
        self.get_message = None

    def send_message(self, test_message):
        json_test_message = json.dumps(self.test_data)
        self.send_message = json_test_message.encode(ENCODING)
        self.get_message = test_message

    def get_message(self):
        json_test_message = json.dumps(self.test_data)
        return json_test_message.encode(ENCODING)


class TestServer(TestCase):
    send_message = {
        ACTION: PRESENCE,
        TIME: 04.04,
        USER: {
            ACCOUNT_NAME: 'Guest'
        }
    }

    response_ok = {RESPONSE: 200}
    response_error = {
        RESPONSE: 400,
        ERROR: 'bad request'
    }

    # def test_send_message(self):
    #     test_sock = TestSock(self.send_message)
    #     send_message(test_sock, self.send_message)
    #     self.assertEqual(test_sock.send_message, test_sock.get_message)

    def test_get_message(self):
        test_sock_ok = TestSock(self.response_ok)
        test_sock_error = TestSock(self.response_error)
        self.assertEqual(recieve_message(test_sock_ok), self.response_ok)
        self.assertEqual(recieve_message(test_sock_error), self.response_error)



if __name__ == '__main__':
    main()
