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
