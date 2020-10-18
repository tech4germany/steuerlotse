import unittest

from app import app
from app.elster.pyeric_dispatcher import run_pyeric, clean_old_folders
from app.utils import gen_random_key

from tests.utils import missing_cert, missing_pyeric_lib


class TestPyericDispatcher(unittest.TestCase):

    @unittest.skipIf(missing_cert(), "skipped because of missing cert.pfx; see pyeric/README.md")
    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_dispatch(self):
        with open('tests/app/elster/sample_with_auth.xml', 'r') as f:
            input_xml = f.read()

        session = gen_random_key()
        result = run_pyeric(input_xml, session, app.config['CERT_PIN'], "ESt_2019")

        self.assertIn(session, str(result.session_folder))

    def test_clean_old_folders(self):
        # TODO: currently manual inspection; devise better testing method
        clean_old_folders(lifetime=10)
