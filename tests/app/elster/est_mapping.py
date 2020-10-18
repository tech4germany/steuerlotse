import unittest
from unittest import result

from app.elster.est_mapping import _check_and_generate_entries
from app.forms.lotse.flow_lotse import LotseMultiStepFlow


class TestEstMapping(unittest.TestCase):

    def test_check_and_generate_entries(self):
        form_data = {
            'person_a_last_name': 'bbb',
            'person_a_first_name': 'aaa',
            'person_a_street': 'wonderwall',
            'person_b_same_address': 'yes',
        }
        results = _check_and_generate_entries(form_data)

        self.assertEqual(results['0100201'], 'bbb')
        self.assertEqual(results['0100301'], 'aaa')
        self.assertEqual(results['0101104'], 'wonderwall')
        self.assertEqual(results['0102105'], 'wonderwall') # copied over to PersonB
