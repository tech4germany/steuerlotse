from babel.numbers import format_decimal
from datetime import date
from decimal import Decimal


UNKNOWN = 'unknown'

# Fields that have a 1:1 correspondence with ELSTER fields
_FORM_TO_FIELD = {
    'person_a_last_name': '0100201',
    'person_a_first_name': '0100301',
    'person_a_dob': '0100401',
    'person_a_street': '0101104',
    'person_a_street_number': '0101206',
    'person_a_street_number_ext': '0101207',
    'person_a_address_ext': '0101301',
    'person_a_plz': '0100601',
    'person_a_town': '0100602',
    'person_a_religion': '0100402',

    # There's no simple logical correlation between field identifiers
    # for Person A and Person B...
    'person_b_last_name': '0100901',
    'person_b_first_name': '0100801',
    'person_b_dob': '0101001',
    'person_b_street': '0102105',
    'person_b_street_number': '0102202',
    'person_b_street_number_ext': '0102203',
    'person_b_address_ext': '0102301',
    'person_b_plz': '0101701',
    'person_b_town': '0101702',
    'person_b_religion': '0101002',

    'iban': '0102102',
}

# Fields that are only to be set if "steuermindernde vortraege" are to be presented
_FORM_STEUERM_TO_FIELDS = {
    'haushaltsnahe_entries': ('0107206',),
    'haushaltsnahe_summe': ('0107207', '0107208'),

    'handwerker_entries': ('0111217',),
    'handwerker_summe': ('0170601', '0170602'),
    'handwerker_lohn_etc_summe': ('0111214', '0111215'),
}

# Fields that do not have a 1:1 correspondence in the form
_EXTRA_FIELDS = {
    'is_einkommensteuererklaerung': '0100001',

    'married_since': '0100701',
    'widowed_since': '0100702',
    'divorced_since': '0100703',
    'separated_since': '0100704',

    'zusammen_veranlagung': '0101201',

    'konto_inhaber_is_person_a': '0101601',

    'belege_werden_nachgereicht': '0100012',
    'is_digitally_signed': '0100013',
}

# Mapping from Religion to ELSTER enumeration value
_RELIGION_LOOKUP = {
    # TODO: add full list, currently only options shown on the `Papiervordruck`
    'ak': '04',
    'ev': '02',
    'rk': '03',
    'none': '11',
}

# Fields that should be rounded to full Euros
_FULL_EURO_FIELDS = {
    'haushaltsnahe_summe',
    'handwerker_summe',
    'handwerker_lohn_etc_summe',
}


def _elsterify(key, value):
    if "_religion" in key:
        return _RELIGION_LOOKUP[value]

    if isinstance(value, str):
        if not value:
            return None  # will exclude empty fields
        return value

    elif isinstance(value, list):
        return ", ".join(value)

    elif isinstance(value, date):
        return value.strftime("%d.%m.%Y")

    elif isinstance(value, Decimal):
        if key in _FULL_EURO_FIELDS:
            return str(int(value))
        return format_decimal(value, locale='de_DE').replace('.', '')

    else:
        return str(value)


def _check_and_generate_entries(form_data, year=2019):
    result = {}

    # Copy over known fields from form
    # - including transformations where required
    # - leaving out fields that are empty
    def copy_to_result(src_data, src_key, dst_field_id):
        value = _elsterify(key, src_data[src_key])
        if value:
            result[dst_field_id] = value

    for key, field_id in _FORM_TO_FIELD.items():
        if key in form_data:
            copy_to_result(form_data, key, field_id)

    # Lebenssituation
    # TODO: might not cover all cases properly yet
    situation = form_data.get('familienstand', None)
    if situation == 'married':
        copy_to_result(form_data, 'familienstand_date', _EXTRA_FIELDS['married_since'])
        result[_EXTRA_FIELDS['zusammen_veranlagung']] = 'X'
    elif situation == 'widowed':
        copy_to_result(form_data, 'familienstand_date', _EXTRA_FIELDS['widowed_since'])
    elif situation == 'divorced':
        copy_to_result(form_data, 'familienstand_date', _EXTRA_FIELDS['divorced_since'])
    elif situation == 'separated':
        copy_to_result(form_data, 'familienstand_date', _EXTRA_FIELDS['separated_since'])

    # Same address
    if form_data.get('person_b_same_address', None) == 'yes':
        copy_dst_src = [
            ('person_b_street', 'person_a_street'),
            ('person_b_street_number', 'person_a_street_number'),
            ('person_b_street_number_ext', 'person_a_street_number_ext'),
            ('person_b_address_ext', 'person_a_address_ext'),
            ('person_b_plz', 'person_a_plz'),
            ('person_b_town', 'person_a_town'),
        ]
        for dst, src in copy_dst_src:
            if _FORM_TO_FIELD[src] in result:
                result[_FORM_TO_FIELD[dst]] = result[_FORM_TO_FIELD[src]]

    # Steuermindernde entries
    if form_data.get('steuerminderung', None) == 'yes':
        for key, field_ids in _FORM_STEUERM_TO_FIELDS.items():
            for field_id in field_ids:
                if key in form_data:
                    copy_to_result(form_data, key, field_id)

    # Add mandatory fields for digital submission
    result[_EXTRA_FIELDS['is_einkommensteuererklaerung']] = 'X'
    result[_EXTRA_FIELDS['konto_inhaber_is_person_a']] = 'X'
    result[_EXTRA_FIELDS['belege_werden_nachgereicht']] = 'X'
    result[_EXTRA_FIELDS['is_digitally_signed']] = 'X'

    return result
