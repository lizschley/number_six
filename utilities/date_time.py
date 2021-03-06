''' Any date or time convenience methods should go here '''
from datetime import datetime, timedelta
from dateutil import tz


def timediff_from_now_for_where(oper='-', units=None):
    '''
    timediff_from_now_for_where takes in variables and returns string of representation of the difference
    between now and the units operator and amount passed in

    :param oper: operator (minus or plus), defaults to '-'
    :type oper: str, optional
    :param units: Expects dictionary, for ex: {'weeks': 12}, defaults to None
    :type units: dictionary, optional
    :return: representation of date figured out to use in where statement
    :rtype: str
    '''
    units = {'days': 1} if units is None else units
    now = datetime.now(tz=tz.tzlocal())
    if oper == '-':
        new_date = str(now - timedelta(**units))
    else:
        new_date = str(now + timedelta(**units))
    return new_date


def current_timestamp_with_timezone():
    '''
    current_timestamp_with_timezone returns the current time in the format to update a
    postgres timestamp with time zone field

    :return: current time with time zone
    :rtype: str
    '''
    now = datetime.now(tz=tz.tzlocal())
    return str(now)


def postgres_friendly_datetime(datetime_obj):
    '''
    postgres_friendly_datetime takes a datetime object and writes it to a string
    in a format that can be used to update postgres
    :param datetime_obj: passed in datetime obj
    :type datetime_obj: datetime.datetime
    :return: string representaion of the object that postgres understands
    :rtype: str
    '''
    string_dt = str(datetime_obj)
    temp = string_dt.split('.')

    return temp[0] + '+00'


def get_current_epoch_date():
    '''
    get_current_epoch_date returns current date in seconds from 1/1/1970 to use for versioning on S3

    :return: epoch date in seconds
    :rtype: int
    '''
    epoch = int(datetime.now().timestamp())
    return epoch
