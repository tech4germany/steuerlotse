import datetime
from decimal import Decimal
import unittest

from app.elster.elster_service import send_with_elster, validate_with_elster
from app.utils import gen_random_key

from tests.utils import missing_cert, missing_pyeric_lib

_BASE_DATA_PERSON_A = {
    'steuernummer': '9198011310010',
    'person_a_dob': datetime.date(1950, 8, 16),
    'person_a_first_name': 'Manfred',
    'person_a_last_name': 'Mustername',
    'person_a_street': 'Steuerweg',
    'person_a_plz': 20354,
    'person_a_town': 'Hamburg',
    'person_a_religion': 'none',
    'iban': 'DE35133713370000012345',
}


_BASE_DATA_PERSON_B = {
    'person_b_dob': datetime.date(1951, 2, 25),
    'person_b_first_name': 'Gerta',
    'person_b_last_name': 'Mustername',
    'person_b_same_address': 'yes',
    'person_b_religion': 'none',
    'person_b_blind': 'no',
}


class TestSampleDataValidation(unittest.TestCase):

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_01_not_married(self):
        form_data = {}
        form_data.update(_BASE_DATA_PERSON_A)

        response = validate_with_elster(form_data, gen_random_key())
        self.assertIsNotNone(response)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_02_married_rel_ev(self):
        form_data = {}
        form_data.update(_BASE_DATA_PERSON_A)
        form_data.update({
            'person_a_religion': 'ev',
            'familienstand': 'married',
            'familienstand_date': datetime.date(2000, 1, 31),
        })

        response = validate_with_elster(form_data, gen_random_key())
        self.assertIsNotNone(response)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_03_divorced_rel_rk(self):
        form_data = {}
        form_data.update(_BASE_DATA_PERSON_A)
        form_data.update({
            'person_a_religion': 'rk',
            'familienstand': 'divorced',
            'familienstand_date': datetime.date(2000, 1, 31),
        })

        response = validate_with_elster(form_data, gen_random_key())
        self.assertIsNotNone(response)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_04_widowed(self):
        form_data = {}
        form_data.update(_BASE_DATA_PERSON_A)
        form_data.update({
            'familienstand': 'widowed',
            'familienstand_date': datetime.date(2000, 1, 31),
        })

        response = validate_with_elster(form_data, gen_random_key())
        self.assertIsNotNone(response)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_05_separated(self):
        form_data = {}
        form_data.update(_BASE_DATA_PERSON_A)
        form_data.update({
            'person_a_religion': 'ev',
            'familienstand': 'separated',
            'familienstand_date': datetime.date(2000, 1, 31),
        })

        response = validate_with_elster(form_data, gen_random_key())
        self.assertIsNotNone(response)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_06_with_person_b_same_address(self):
        form_data = {}
        form_data.update(_BASE_DATA_PERSON_A)
        form_data.update(_BASE_DATA_PERSON_B)
        form_data.update({
            'familienstand': 'married',
            'familienstand_date': datetime.date(2000, 1, 31),
        })

        response = validate_with_elster(form_data, gen_random_key())
        self.assertIsNotNone(response)

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_07_steuerminderungen(self):
        form_data = {}
        form_data.update(_BASE_DATA_PERSON_A)
        form_data.update({
            'steuerminderung': 'yes',

            'haushaltsnahe_entries': ["Gartenarbeiten"],
            'haushaltsnahe_summe': Decimal('500.00'),

            'handwerker_entries': ["Renovierung Badezimmer"],
            'handwerker_summe': Decimal('200.00'),
            'handwerker_lohn_etc_summe': Decimal('100.00'),
        })

        response = send_with_elster(form_data, "test")
        self.assertIsNotNone(response)
