from collections import namedtuple

from erica.config import get_settings

TransferHeaderFields = namedtuple(
    'TransferHeaderFields',
    ['datenart', 'testmerker', 'herstellerId', 'verfahren', 'datenLieferant']
)

_HERSTELLER_ID = get_settings().hersteller_id
_DATENLIEFERANT = get_settings().elster_datenlieferant


def get_est_th_fields(use_testmerker):
    return TransferHeaderFields(
        datenart='ESt',
        testmerker=_get_testmerker('ElsterErklaerung', use_testmerker),
        herstellerId=_HERSTELLER_ID,
        verfahren='ElsterErklaerung',
        datenLieferant=_DATENLIEFERANT,
    )


def get_vast_request_th_fields(use_testmerker):
    return TransferHeaderFields(
        datenart='SpezRechtAntrag',
        testmerker=_get_testmerker('ElsterBRM', use_testmerker),
        herstellerId=_HERSTELLER_ID,
        verfahren='ElsterBRM',
        datenLieferant=_DATENLIEFERANT,
    )


def get_vast_activation_th_fields(use_testmerker):
    return TransferHeaderFields(
        datenart='SpezRechtFreischaltung',
        testmerker=_get_testmerker('ElsterBRM', use_testmerker),
        herstellerId=_HERSTELLER_ID,
        verfahren='ElsterBRM',
        datenLieferant=_DATENLIEFERANT,
    )


def get_vast_revocation_th_fields(use_testmerker):
    return TransferHeaderFields(
        datenart='SpezRechtStorno',
        testmerker=_get_testmerker('ElsterBRM', use_testmerker),
        herstellerId=_HERSTELLER_ID,
        verfahren='ElsterBRM',
        datenLieferant=_DATENLIEFERANT,
    )


def get_vast_list_th_fields(use_testmerker):
    return TransferHeaderFields(
        datenart='SpezRechtListe',
        testmerker=_get_testmerker('ElsterBRM', use_testmerker),
        herstellerId=_HERSTELLER_ID,
        verfahren='ElsterBRM',
        datenLieferant=_DATENLIEFERANT,
    )


def get_vast_beleg_ids_request_th_fields(use_testmerker):
    return TransferHeaderFields(
        datenart='ElsterVaStDaten',
        testmerker=_get_testmerker('ElsterDatenabholung', use_testmerker),
        herstellerId=_HERSTELLER_ID,
        verfahren='ElsterDatenabholung',
        datenLieferant=_DATENLIEFERANT,
    )


def get_abrufcode_th_fields(use_testmerker):
    return TransferHeaderFields(
        datenart='AbrufcodeAntrag',
        testmerker=_get_testmerker('ElsterSignatur', use_testmerker),
        herstellerId=_HERSTELLER_ID,
        verfahren='ElsterSignatur',
        datenLieferant=_DATENLIEFERANT,
    )


def get_vast_beleg_request_th_fields(use_testmerker):
    return TransferHeaderFields(
        datenart='ElsterVaStDaten',
        testmerker=_get_testmerker('ElsterDatenabholung', use_testmerker),
        herstellerId=_HERSTELLER_ID,
        verfahren='ElsterDatenabholung',
        datenLieferant=_DATENLIEFERANT,
    )


def _get_testmerker(verfahren, use_testmerker):
    _TESTMERKER = {
        'ElsterErklaerung': '700000004',
        'ElsterDatenabholung': '370000001',
        'ElsterBRM': '370000001',
        'ElsterSignatur': '080000001'
    }
    if get_settings().use_testmerker or use_testmerker:
        return _TESTMERKER[verfahren]
    else:
        return ''
