import pytz
import decimal
from flask import json


def to_est(dt):
    utc_dt = pytz.utc.localize(dt)
    est = pytz.timezone('US/Eastern')
    return utc_dt.astimezone(est)


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)
    

