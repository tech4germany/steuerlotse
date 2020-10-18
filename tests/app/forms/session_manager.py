import unittest

from app.forms.session_manager import SessionManager

from decimal import Decimal
from datetime import date


class TestSessionMananger(unittest.TestCase):

    def test_json_encode_decode(self):
        sm = SessionManager()

        data = {
            'test_string': 'test',
            'test_date': date(2020, 1, 31),
            'test_decimal': Decimal('42.00')
        }

        json = sm._to_json(data)
        data_2 = sm._from_json(json)

        self.assertEqual(data, data_2)
