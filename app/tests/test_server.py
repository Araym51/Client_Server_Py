import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from app.common.constants import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from app.server_app import process_client_message

class TestServer(unittest.TestCase):
    error_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


if __name__ == '__main__':
    unittest.main()