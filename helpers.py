from datetime import datetime
import pytz
from app import app


def to_est(dt):
    utc_dt = pytz.utc.localize(dt)
    est = pytz.timezone('US/Eastern')
    return utc_dt.astimezone(est)


@app.context_processor
def inject_to_est():
    return {'to_est': to_est}