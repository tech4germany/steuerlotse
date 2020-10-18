import secrets

from schwifty import IBAN
from flask_babel import _
from xml.dom import minidom


def validate_iban(string):
    try:
        iban = IBAN(string)
    except ValueError:
        raise ValueError(_('utils.validate-iban.invalid-iban'))

    if iban.country_code != 'DE':
        raise ValueError(_('utils.validate-iban.country-code-not-de'))

    return iban.formatted


def pretty_xml(xml_string):
    return minidom.parseString(xml_string).toprettyxml(indent=" "*4)


def gen_random_key(length=32):
    return secrets.token_urlsafe(length)
