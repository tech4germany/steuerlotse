import unittest

from app.elster.elster_service import _t4g_vorsatz, send_with_elster
from app.forms.lotse.flow_lotse import LotseMultiStepFlow, MultiStepFlow
from app.utils import gen_random_key

from tests.utils import missing_cert, missing_pyeric_lib


class TestElsterService(unittest.TestCase):

    def test_t4g_vorsatz(self):
        vorsatz = _t4g_vorsatz(steuernummer='123', year=2019)
        self.assertTrue(vorsatz.Erstelldatum.startswith('202'))

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_full_form_to_elster_run(self):
        form_data = LotseMultiStepFlow(None).debug_data()[1]
        session_id = gen_random_key()

        response = send_with_elster(form_data, session_id)
        self.assertIsNotNone(response)
