from passlib.hash import bcrypt

from app import app
from app.crypto.mock_pw_hashing import MockGlobalSaltHash, MockIndivSaltHash


class InvalidHashAlgortihmError(Exception):
    """ Exception raised when the config includes an invalid value for HASH_ALGORITHM."""


def global_salt_hash():
    if app.config['HASH_ALGORITHM'] == 'mock':
        return MockGlobalSaltHash()
    elif app.config['HASH_ALGORITHM'] == 'bcrypt':
        return bcrypt.using(salt=app.config['IDNR_SALT'])
    else:
        raise InvalidHashAlgortihmError


def indiv_salt_hash():
    if app.config['HASH_ALGORITHM'] == 'mock':
        return MockIndivSaltHash()
    elif app.config['HASH_ALGORITHM'] == 'bcrypt':
        return bcrypt.using()
    else:
        raise InvalidHashAlgortihmError
