from datetime import datetime, timedelta
import pytz


def datetime_str(config={}):
    newdate = datetime.now(pytz.timezone('US/Pacific'))
    if 'hours' in config:
        startdate = newdate + timedelta(hours=config['hours'])

    def thegenerator():
        newdate = startdate + timedelta(hours=1)
        val = newdate.replace(microsecond=0).isoformat()
        while(True):
            yield val
    return thegenerator


def dategen(config):
    return datetime_str(config)()


GENERATORS = {'dategen': dategen}
