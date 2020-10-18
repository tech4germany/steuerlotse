from app.elster import elster_xml, est_mapping, pyeric_dispatcher
from app import app

from datetime import datetime

_DEFAULT_PIN = app.config['CERT_PIN']


def _t4g_vorsatz(steuernummer, year):
    """Creates a `Vorsatz` for Elster XML with defaults set for T4G."""
    _now = datetime.now()
    creation_date = _now.strftime('%Y%m%d')
    creation_time = _now.strftime('%H%M%S')

    return elster_xml.Vorsatz(
        unterfallart='10', ordNrArt='S', vorgang='01',
        StNr=steuernummer,
        Zeitraum=str(year),
        Erstelldatum=creation_date,
        Erstellzeit=creation_time,
        AbsName='Testfall ERiC von T4G',
        AbsStr='Zionkirchstr 73a',
        AbsPlz='10119',
        AbsOrt='Berlin',
        Copyright='(C) 2009 ELSTER, (C) 2020 T4G',
    )

def validate_with_elster(form_data, session_id, year=2019):
    return send_with_elster(form_data, session_id, year, only_validate=True)

def send_with_elster(form_data, session_id, year=2019, only_validate=False):
    """The overarching method that is being called from the web backend. It
    will map the form data to Elster field identifiers, then generate the XML,
    and processes and sends it in a sub-process using ERiC.
    """
    verfahren = 'ESt_%s' % str(year)

    # Translate our form data structure into the fields from
    # the Elster specification (see `Jahresdokumentation_10_2019.xml`)
    fields = est_mapping._check_and_generate_entries(form_data)

    # Generate the full XML from this
    vorsatz = _t4g_vorsatz(steuernummer=form_data['steuernummer'], year=year)
    xml = elster_xml.generate_full_xml(vorsatz, fields)

    # Handover to PyERiC outside this process for sending
    response = pyeric_dispatcher.run_pyeric(xml, session_id, _DEFAULT_PIN, verfahren, only_validate)

    return response
