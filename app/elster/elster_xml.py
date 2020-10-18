from pyeric import EricApi

from collections import namedtuple
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, XML
from xml.dom import minidom

import xml.etree.ElementTree as ET

Vorsatz = namedtuple(
    'Vorsatz',
    [
        'unterfallart', 'ordNrArt', 'vorgang',
        'StNr',
        'Zeitraum',
        'Erstelldatum', 'Erstellzeit',
        'AbsName', 'AbsStr', 'AbsPlz', 'AbsOrt',
        'Copyright',
    ]
)

TransferHeaderFields = namedtuple(
    'TransferHeaderFields',
    ['datenart', 'testmerker', 'herstellerId', 'datenLieferant']
)

_TEST_TH_FIELDS = TransferHeaderFields(
    datenart='ESt',
    testmerker='700000004',
    herstellerId='74931',
    datenLieferant='Softwaretester ERiC',
)


def _pretty(xml, remove_decl=True):
    """Pretty prints a etree xml object."""
    xml = minidom.parseString(tostring(xml))
    if remove_decl:
        xml = xml.childNodes[0]
    return xml.toprettyxml(indent=" "*4)


def _add_xml_nutzdaten_header(xml_top, nutzdaten_ticket, empfaenger, version="11", empfaenger_id="F"):
    """Adds the <NutzdatenHeader> element to the given `xml_top` element."""
    xml_ndh = SubElement(xml_top, 'NutzdatenHeader', version=version)
    SubElement(xml_ndh, 'NutzdatenTicket').text = nutzdaten_ticket
    SubElement(xml_ndh, 'Empfaenger', id=empfaenger_id).text = empfaenger


def _add_xml_vorsatz(xml_top, vorsatz):
    """Adds the <Vorsatz> element to the given `xml_top` element."""
    xml_vorsatz = SubElement(
        xml_top, 'Vorsatz',
        unterfallart=vorsatz.unterfallart, ordNrArt=vorsatz.ordNrArt, vorgang=vorsatz.vorgang,
    )
    SubElement(xml_vorsatz, 'StNr').text = vorsatz.StNr
    SubElement(xml_vorsatz, 'Zeitraum').text = vorsatz.Zeitraum
    SubElement(xml_vorsatz, 'Erstelldatum').text = vorsatz.Erstelldatum
    SubElement(xml_vorsatz, 'Erstellzeit').text = vorsatz.Erstellzeit
    SubElement(xml_vorsatz, 'AbsName').text = vorsatz.AbsName
    SubElement(xml_vorsatz, 'AbsStr').text = vorsatz.AbsStr
    SubElement(xml_vorsatz, 'AbsPlz').text = vorsatz.AbsPlz
    SubElement(xml_vorsatz, 'AbsOrt').text = vorsatz.AbsOrt
    SubElement(xml_vorsatz, 'Copyright').text = vorsatz.Copyright
    SubElement(xml_vorsatz, 'Rueckuebermittlung', bescheid='nein').text = ""


def _add_xml_field(xml_top, nr, wert, index='01', lfdNr='00001'):
    """Adds a <Feld> element to the given `xml_top` element. These are used by 
    Elster to somewhat emulate CSV in XML \o/. The `index` and `lfdNr` fields
    are explained in the `Entwicklerhandbuch`, but for our prototype we usually
    don't have to change them."""
    SubElement(xml_top, 'Feld', index=index, lfdNr=lfdNr, nr=nr, wert=wert)


def _add_xml_fields(xml_top, fields):
    for nr, wert in fields.items():
        _add_xml_field(xml_top, nr, wert)


def generate_xml_nutzdaten(vorsatz, fields, nutzdaten_ticket, empfaenger, version='2'):
    """Generates the entire <Nutzdatenblock> using the given `vorsatz` and `fields`."""
    xml_top = Element('Nutzdatenblock')
    _add_xml_nutzdaten_header(xml_top, nutzdaten_ticket, empfaenger)

    xml_nutzdaten = SubElement(xml_top, 'Nutzdaten')
    xml_erklaerung = SubElement(xml_nutzdaten, 'Jahressteuererklaerung', version=version)
    _add_xml_vorsatz(xml_erklaerung, vorsatz)
    _add_xml_fields(xml_erklaerung, fields)

    return xml_top


_BASE_XML = """<Elster xmlns="http://www.elster.de/elsterxml/schema/v11"></Elster>
"""


def generate_full_xml(vorsatz, fields, nutzdaten_ticket="default_nutzdaten_ticket", empfaenger="9198", th_fields=_TEST_TH_FIELDS):
    """Generates the full XML for the given `vorsatz` and `fields`. In a first step the
    <Nutzdaten> part is generated before the ERiC library is called for generating the
    proper <TransferHeader>.
    """

    # Generate the content bits
    ET.register_namespace('', "http://www.elster.de/elsterxml/schema/v11")
    nutzdaten = generate_xml_nutzdaten(vorsatz, fields, nutzdaten_ticket, empfaenger)

    # Load into ELSTER base XML
    base_xml = XML(_BASE_XML)
    datenteil_xml = Element('DatenTeil')
    datenteil_xml.append(nutzdaten)
    base_xml.append(datenteil_xml)

    # Generate TransferHeader using ERiC
    xml_string = _pretty(base_xml, remove_decl=False)

    eric = EricApi(debug=False)
    try:
        eric.initialise()
        xml_string_with_th = eric.create_th(
            xml_string,
            datenart=th_fields.datenart, testmerker=th_fields.testmerker,
            herstellerId=th_fields.herstellerId, datenLieferant=th_fields.datenLieferant)
    finally:
        eric.shutdown()

    return xml_string_with_th.decode()
