from app import app
from app.utils import gen_random_key
from cachetools import TTLCache
from datetime import date, datetime
from decimal import Decimal

import decimal
import json


class SessionManager(object):
    """The SessionManager allows to keep a form state for a given identifier. It
    uses the TLL value to remove old entries (usually 10 min). This here
    is an abstract class. The application either uses `InMemorySessionManager`
    or the `MongoDbSessionManager`.
    """

    def get_or_create(self, identifier, default_data={}):
        """Returns the data associated with the `identifier`. If the
        identifier is unknown, a new entry will be created with the
        given `default_data` and returned. In each case the TTL countdown
        will be reset.
        """
        if identifier:
            json = self._load_session(identifier)
            if json != None:
                return identifier, self._from_json(json)

        # If no identifier provided or no entry
        # -> create new one with empty data
        identifier = gen_random_key()
        if self._has_session(identifier):
            # TODO handle properly
            raise KeyError("key collision")

        data = default_data
        json = self._to_json(data)
        self._save_session(identifier, json)

        return identifier, data

    def update(self, identifier, data):
        """Updates the data for the given identifier."""
        json = self._to_json(data)
        self._save_session(identifier, json)

    def has_session(self, identifier):
        return self._has_session(identifier)

    def _load_session(self, identifier):
        raise NotImplementedError()

    def _save_session(self, identifier, json):
        raise NotImplementedError()

    def _has_session(self, identifier):
        raise NotImplementedError()

    # TODO: ugly hack as MongoDB cannot serialize
    # datetime.date and decimal.Decimal
    def _to_json(self, d):
        return json.dumps(d, cls=_JsonEncoder)

    def _from_json(self, j):
        return json.loads(j, cls=_JsonDecoder)


class _JsonEncoder(json.JSONEncoder):
    """JsonEncoder allowing serialising `Decimal` and `datetime.date` objects."""

    def default(self, o):
        if isinstance(o, Decimal):
            return {
                "_type": "decimal",
                "v": str(o),
            }
        elif isinstance(o, date):
            return {
                "_type": "date",
                "y": o.year,
                "m": o.month,
                "d": o.day,
            }
        return super(_JsonEncoder, self).default(o)


class _JsonDecoder(json.JSONDecoder):
    """JsonDecoder allowing deserialising `Decimal` and `datetime.date` objects."""

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if '_type' not in obj:
            return obj
        _type = obj['_type']
        if _type == 'date':
            return date(obj['y'], obj['m'], obj['d'])
        elif _type == 'decimal':
            return decimal.Decimal(obj['v'])


_GLOBAL_CACHE = None


class InMemorySessionManager(SessionManager):
    """An in-memory session manager implementation that uses a simple `TTLCache`.
    It will not work in production, as `gunicorn` spawns separate processes that
    do not share the same memory."""

    def __init__(self):
        global _GLOBAL_CACHE

        if not _GLOBAL_CACHE:
            _GLOBAL_CACHE = TTLCache(maxsize=100_000, ttl=app.config['SESSION_TTL_SECONDS'])
        self.cache = _GLOBAL_CACHE

    def _load_session(self, identifier):
        return self.cache.get(identifier)

    def _save_session(self, identifier, json):
        self.cache[identifier] = json

    def _has_session(self, identifier):
        return identifier in self.cache


class MongoDbSessionManager(SessionManager):
    """A session manager implementation that uses MongoDB. The expiration of items
    is ensured through an index with the `expireAfterSeconds` property.
    """

    def __init__(self):
        from app import mongo
        self._ensure_database(mongo)
        self.collection = mongo.db.sessions

    def _ensure_database(self, mongo):
        mongo.db.sessions.create_index("last_update", expireAfterSeconds=app.config['SESSION_TTL_SECONDS'])

    def _load_session(self, identifier):
        res = self.collection.find_one({'_id': identifier})
        if not res:
            return None

        self.collection.update_one(
            {'_id': identifier},
            {"$set": {'last_update': datetime.utcnow()}
             })
        return res['json']

    def _save_session(self, identifier, json):
        if self._has_session(identifier):
            self.collection.update_one(
                {'_id': identifier},
                {"$set": {
                    'json': json,
                    'last_update': datetime.utcnow()
                }}
            )
        else:
            self.collection.insert_one({
                '_id': identifier,
                'json': json,
                'last_update': datetime.utcnow()
            })

    def _has_session(self, identifier):
        return self.collection.count_documents({'_id': identifier}) > 0
