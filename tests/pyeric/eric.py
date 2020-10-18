import unittest

from pyeric.eric import EricApi

from tests.utils import missing_pyeric_lib


class TestEricBasicSanity(unittest.TestCase):

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_api_creation_and_initialise(self):
        api = EricApi(debug=False)
        api.initialise()

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_api_create_buffer(self):
        api = EricApi(debug=False)
        buf = api.create_buffer()
        api.close_buffer(buf)
