import unittest

from app.forms.lotse.flow_lotse import *

class TestFlowLotse(unittest.TestCase):
    
    def test_debug_data_non_empty(self):
        flow = LotseMultiStepFlow(endpoint='')
        debug_data = flow.debug_data()

        self.assertIsNotNone(debug_data[0])
        self.assertIsNotNone(debug_data[1])