import shutil
import subprocess
import os
import time

from app import app
from collections import namedtuple
from xml.dom.minidom import parseString

_INSTANCES_FOLDER = os.path.join('pyeric', 'instances')
_BLUEPRINT_FOLDER = os.path.join(_INSTANCES_FOLDER, 'blueprint')
_SESSION_FOLDER_PREFIX = 'session_'


def clean_old_folders(lifetime=None):
    if not lifetime:
        lifetime = app.config['SESSION_TTL_SECONDS']

    cut_off_time = int(time.time()) - lifetime

    for root, dirs, _ in os.walk(_INSTANCES_FOLDER):
        for dir in dirs:
            if not dir.startswith(_SESSION_FOLDER_PREFIX):
                continue  # only consider our session folders

            dir_path = os.path.join(root, dir)
            timestamp = os.path.getmtime(dir_path)
            if timestamp < cut_off_time:
                shutil.rmtree(dir_path)


PyEricResponse = namedtuple(
    'PyEricResponse',
    ['session_folder']
)


def _get_session_folder(session_id):
    return os.path.abspath(os.path.join(_INSTANCES_FOLDER, _SESSION_FOLDER_PREFIX + session_id))


def run_pyeric(input_xml, session_id, cert_pin, verfahren, only_validate=False):
    session_folder = _get_session_folder(session_id)
    if not os.path.exists(session_folder):
        os.mkdir(session_folder)

    # fill new session folder
    with open(os.path.join(session_folder, 'input.xml'), 'w') as f:
        f.write(input_xml)

    shutil.copyfile(
        os.path.join(_BLUEPRINT_FOLDER, 'cert.pfx'),
        os.path.join(session_folder, 'cert.pfx'))

    # run eric client in a new process
    args = ['python3', 'pyeric/eric_client.py',
            '--work-dir', session_folder,
            '--cert-pin', cert_pin,
            '--verfahren', verfahren]
    if only_validate:
        args.append('--only-validate')
    subprocess.check_call(args)

    return PyEricResponse(session_folder)


def was_successful(session):
    return os.path.exists(get_pdf_path(session))


def get_pdf_path(session):
    session_folder = _get_session_folder(session)
    return os.path.join(session_folder, 'print.pdf')


def get_transfer_ticket(server_response):
    try:
        xml = parseString(server_response)
        return xml.documentElement.getElementsByTagName('TransferHeader')[0].getElementsByTagName('TransferTicket')[0].childNodes[0].nodeValue
    except Exception:  # intentional generic catch
        return "failure"


def get_eric_response(session):
    session_folder = _get_session_folder(session)
    try:
        with open(os.path.join(session_folder, 'eric_response.xml'), 'r') as f:
            return f.read()
    except Exception:  # intentional generic catch
        return ""


def get_server_response(session):
    session_folder = _get_session_folder(session)
    try:
        with open(os.path.join(session_folder, 'server_response.xml'), 'r') as f:
            return f.read()
    except Exception:  # intentional generic catch
        return ""
