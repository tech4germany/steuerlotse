from datetime import date
from decimal import Decimal

from flask.json import JSONEncoder, JSONDecoder


class SteuerlotseJSONEncoder(JSONEncoder):
    """JsonEncoder allowing serializing `Decimal` and `datetime.date` objects."""

    def default(self, obj):
        if isinstance(obj, Decimal):
            return {
                "_type": "decimal",
                "v": str(obj),
            }
        elif isinstance(obj, date):
            return {
                "_type": "date",
                "y": obj.year,
                "m": obj.month,
                "d": obj.day,
            }
        return super(SteuerlotseJSONEncoder, self).default(obj)


class SteuerlotseJSONDecoder(JSONDecoder):
    """JsonDecoder allowing deserializing `Decimal` and `datetime.date` objects."""

    def __init__(self, *args, **kwargs):
        self.flask_object_hook = kwargs.get('object_hook')
        kwargs['object_hook'] = self.steuerlotse_object_hook
        JSONDecoder.__init__(self, *args, **kwargs)

    def steuerlotse_object_hook(self, obj):
        if '_type' not in obj:
            if self.flask_object_hook:
                return self.flask_object_hook(obj)
            else:
                return obj
        _type = obj['_type']
        if _type == 'date':
            return date(obj['y'], obj['m'], obj['d'])
        elif _type == 'decimal':
            return Decimal(obj['v'])
