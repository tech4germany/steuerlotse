import unittest
from unittest import result

from app.elster.elster_xml import Vorsatz, _add_xml_vorsatz, _add_xml_fields, generate_xml_nutzdaten, generate_full_xml
from xml.etree.ElementTree import Element, tostring

from tests.utils import missing_pyeric_lib


class TestElsterXml(unittest.TestCase):

    def _dummy_vorsatz(self):
        return Vorsatz(
            unterfallart='10',
            ordNrArt='S',
            vorgang='01',
            StNr='9198011310010',
            Zeitraum='2019',
            Erstelldatum='20201007',
            Erstellzeit='181550',
            AbsName='Testfall ERiC',
            AbsStr='Teststrasse 42',
            AbsPlz='12345',
            AbsOrt='Berlin',
            Copyright='(C) 2009 ELSTER, (C) 2020 T4G',
        )

    def _dummy_fields(self):
        return {
            '0100201': 'Maier',
            '0100301': 'Hans',
            '0100401': '05.05.1955',
            '0100602': 'Musterort',
        }

    def test_add_vorsatz(self):
        xml_top = Element('main')
        _add_xml_vorsatz(xml_top,  self._dummy_vorsatz())
        xml_string = tostring(xml_top).decode()

        self.assertIn("<StNr>9198011310010</StNr>", xml_string)
        self.assertIn("<Zeitraum>2019</Zeitraum>", xml_string)
        self.assertIn("<Erstelldatum>20201007</Erstelldatum>", xml_string)
        self.assertIn("<Erstellzeit>181550</Erstellzeit>", xml_string)
        self.assertIn("<AbsName>Testfall ERiC</AbsName>", xml_string)
        self.assertIn("<AbsStr>Teststrasse 42</AbsStr>", xml_string)
        self.assertIn("<AbsPlz>12345</AbsPlz>", xml_string)
        self.assertIn("<AbsOrt>Berlin</AbsOrt>", xml_string)
        self.assertIn("<Copyright>(C) 2009 ELSTER, (C) 2020 T4G</Copyright>", xml_string)
        self.assertIn('<Rueckuebermittlung bescheid="nein"', xml_string)

    def test_add_fields(self):
        xml_top = Element('main')
        _add_xml_fields(xml_top,  self._dummy_fields())
        xml_string = tostring(xml_top).decode()

        self.assertIn('<Feld index="01" lfdNr="00001" nr="0100201" wert="Maier"', xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_generate_nutzdaten(self):
        xml = generate_xml_nutzdaten(
            vorsatz=self._dummy_vorsatz(),
            fields=self._dummy_fields(),
            nutzdaten_ticket='nutzdatenTicket123',
            empfaenger='9198')
        xml_string = tostring(xml).decode()

        self.assertIn("<StNr>9198011310010</StNr>", xml_string)
        self.assertIn('<Feld index="01" lfdNr="00001" nr="0100201" wert="Maier"', xml_string)
        self.assertIn("<NutzdatenTicket>nutzdatenTicket123</NutzdatenTicket>", xml_string)
        self.assertIn('<Empfaenger id="F">9198</Empfaenger>', xml_string)

    @unittest.skipIf(missing_pyeric_lib(), "skipped because of missing eric lib; see pyeric/README.md")
    def test_full_xml(self):
        xml_string = generate_full_xml(
            vorsatz=self._dummy_vorsatz(),
            fields=self._dummy_fields(),
            nutzdaten_ticket='nutzdatenTicket123',
            empfaenger='9198')

        # Check Transfer Header
        self.assertIn("<DatenArt>ESt</DatenArt>", xml_string)
        self.assertIn("<HerstellerID>74931</HerstellerID>", xml_string)

        # Check for Vorsatz and fields
        self.assertIn("<StNr>9198011310010</StNr>", xml_string)
        self.assertIn('<Feld index="01" lfdNr="00001" nr="0100201" wert="Maier"', xml_string)
