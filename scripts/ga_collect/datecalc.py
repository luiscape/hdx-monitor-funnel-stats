__author__ = 'Godfrey Takavarasha'

import calendar
import datetime
#from datetime import date
#from datetime import timedelta


__Thirty_Day_Months = [4, 6, 9, 11]
__Digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


class PeriodTypes:
    """ Provides a named list of the period types used in the module

    """
    Year = 'y'
    Quarter = 'q'
    Month = 'm'
    Week = 'w'
    Day = 'd'

    Allowed_Period_Types = [Day, Week, Month, Quarter, Year]


def __validate_period_type(period_type):
    """ Validates the supplied period type and returns the validated period type

    The returned period type is always lowercase.

    :param period_type: str: the period type to check
    :return: str: the valid period type
    """
    if not period_type:
        raise ValueError('period type is required')
    else:
        flag = period_type[0:].lower()

        if flag in PeriodTypes.Allowed_Period_Types:
            return flag
        else:
            message = ''
            for item in PeriodTypes.Allowed_Period_Types:
                message += ", '{0}'".format(item)
            message = "'{0}' is not a valid period type. Period type must be one of " + message[2:]

            raise ValueError(message.format(period_type,))


def get_period(date, period_type):
    """ Returns the period that the specified date falls in

    :param date: The date whose period is to be determined
    :param period_type: The period type
    :return: str: the period
    """

    # Check that the period type is in range.
    # validate_period_type will throw an exception if the flag is not valid
    flag = __validate_period_type(period_type)

    if flag == PeriodTypes.Day:
        return date.isoformat()
    elif flag == PeriodTypes.Week:
        return "{year:04}-W{week:02}".format(year=date.year, week=date.isocalendar()[1])
    elif flag == PeriodTypes.Month:
        return "{year:04}-{month:02}".format(year=date.year, month=date.month)
    elif flag == PeriodTypes.Quarter:
        return "{year:04}-Q{quarter_num:01}".format(year=date.year, quarter_num=quarter_num(date))
    elif flag == PeriodTypes.Year:
        return "{year:04}".format(year=date.year,)


def period_start_date(date, period_type):
    """ Returns the start date of the period in which date d falls

    :param date: the date
    :param period_type: the period type
    :return: date: the start date of the period
    """

    # Check that the period type is in range.
    flag = __validate_period_type(period_type)

    if flag == PeriodTypes.Day:
        return date
    elif flag == PeriodTypes.Week:
        return date - datetime.timedelta(days=date.isocalendar()[2] - 1)
    elif flag == PeriodTypes.Month:
        return date.replace(day=1)
    elif flag == PeriodTypes.Quarter:
        if quarter_num(date) == 1:
            return date.replace(month=1, day=1)
        elif quarter_num(date) == 2:
            return date.replace(month=4, day=1)
        elif quarter_num(date) == 3:
            return date.replace(month=7, day=1)
        else:
            return date.replace(month=10, day=1)
    elif flag == PeriodTypes.Year:
        return date.replace(month=1, day=1)


def period_end_date(date, period_type):
    """ Returns the start date of the period in which date date falls

    :param date: the date
    :param type: the period type
    :return: date: the start date of the period
    """

    # Check that the period type is in range.
    # __validate_ptype will throw an exception if the flag is not valid
    flag = __validate_period_type(period_type)

    if flag == PeriodTypes.Day:
        return date
    elif flag == PeriodTypes.Week:
        return period_start_date(date, flag) + datetime.timedelta(days=6)
    elif flag == PeriodTypes.Month:
        return __month_end(date)
    elif flag == PeriodTypes.Quarter:
        if quarter_num(date) == 1:
            return date.replace(month=3, day=31)
        elif quarter_num(date) == 2:
            return date.replace(month=6, day=30)
        elif quarter_num(date) == 3:
            return date.replace(month=9, day=30)
        else:
            return date.replace(month=12, day=31)
    elif flag == PeriodTypes.Year:
        return date.replace(month=12, day=31)


def __is_month_end(date):
    """ Returns True if the given date falls on the last day of the month, False otherwise

    :param date: the date to test
    :return: bool: True if given date is monthend, False otherwise
    """
    if date.month == 2:
        if calendar.isleap(date.year):
            return date.day == 29
        else:
            return date.day == 28
    elif date.month in __Thirty_Day_Months:
        return date.day == 30
    else:
        return date.day == 31


def __month_end(date):
    """ Returns the month end date of the given date

    :param date: the date whose month-end date will be returned
    :return: date: the month-end date
    """
    if date.month == 2:
        if calendar.isleap(date.year):
            return date.replace(day=29)
        else:
            return date.replace(day=28)
    elif date.month in __Thirty_Day_Months:
        return date.replace(day=30)
    else:
        return date.replace(day=31)


def add_months(date, months):
    """ Adds [months] number of calendar months to date object [date] and returns the result

    :param date: the date to add months to
    :param months: the number of months to add
    :return: date: the date when [months] number of months is added to [date]
    """
    num_of_years = abs(months) // 12
    num_of_months = abs(months) % 12

    sign = 1
    if months < 0:
        sign = - 1

    new_year = date.year + (num_of_years * sign)
    new_month = date.month + (num_of_months * sign)

    # Adjust month and year for any overflow (and underflow) that may take place.
    if new_month < 1:
        new_year -= 1
        new_month += 12
    elif new_month > 12:
        new_year += 1
        new_month -= 12

    new_day = date.day

    # If original date was a month end, the result should also be on a month end
    if __is_month_end(date):
        new_day = __month_end(datetime.date(year=new_year, month=new_month, day=1)).day

    elif new_month == 2 and new_day > 28:
        # For feb, all days past the 28th, the new day will default to the month end
        new_day = __month_end(date(year=new_year, month=new_month, day=1)).day
    elif new_day > 30 and new_month in __Thirty_Day_Months:
        # For 30 day months, adjust last day to 30 if necessary
        new_day = 30

    return datetime.date(year=new_year, month=new_month, day=new_day)


def quarter_num(date):
    """ Returns the quarter number in which a given date falls

    The quarter returned is a number between 1 and 4 (inclusive)

    :param date: a date object
    :return: int: the quarter
    """
    if date.month in [1, 2, 3]:
        return 1
    elif date.month in [4, 5, 6]:
        return 2
    elif date.month in [7, 8, 9]:
        return 3
    else:
        return 4


def get_period_type(period):
    """ Returns the period type of the given period

    :param period: str: the period to test
    :return: str: the period type of period
    """
    if __is_year_period(period):
        return PeriodTypes.Year

    if __is_quarter_period(period):
        return PeriodTypes.Quarter

    if __is_month_period(period):
        return PeriodTypes.Month

    if __is_week_period(period):
        return PeriodTypes.Week

    if __is_day_period(period):
        return PeriodTypes.Day

    return None
    

def __is_year_period(s):
    """ Returns True if s is a year period, False otherwise

    s is a year period if it is exactly four digits long

    :param s: 
    :return:
    """

    return len(s) == 4 and \
        s[0] in __Digits and \
        s[1] in __Digits and \
        s[2] in __Digits and \
        s[3] in __Digits


def __is_quarter_period(s):
    """ Returns True if s is a quarter period

    s is a quarter period if it begins with a year period, followed by the literal "-Q" and ends with a
    single digit 1 and 4 (inclusive). Examples

    >>> is_quarter_period('2015-Q1')
    True

    >>> is_quarter_period('2015-Q01')
    False

    :param s: str
    :return:
    """

    return len(s) == 7 and \
        __is_year_period(s[:4]) and \
        s[4:6] == '-Q' and \
        s[6] in ['1', '2', '3', '4']


def __is_month_period(s):
    """ Returns True if s is a month period

    s is a month period if it begins with a year period, followed by the literal "-" and ends with a
    2 digit number between 01 and 12 (inclusive). Examples

    >>> is_month_period('2015-03')
    True

    >>> is_quarter_period('2015-3')
    False

    :param s: str
    :return:
    """

    return len(s) == 7 and \
        __is_year_period(s[:4]) and \
        s[4] == '-' and \
        s[5] in ['0', '1'] and \
        s[6] in __Digits and \
        0 < int(s[-2:]) <= 12


def __is_week_period(s):
    """ Returns True if and only if s is a week period

    s is a week period if it begins with a year period, followed by the literal "-W" and end with a
    2 digit number between 01 and 53 (inclusive). The ending week number must exist in the year.
    Examples

    >>> is_week_period('2015-W05')
    True

    >>> is_week_period('2015-W5')
    False

    :param s: str
    :return:
    """

    return len(s) == 8 and \
        __is_year_period(s[:4]) and \
        s[4:6] == '-W' and \
        s[6] in ['0', '1', '2', '3', '4', '5'] and \
        s[7] in __Digits and \
        int(s[-2:]) > 0 and \
        (int(s[-2:]) <= datetime.date(int(s[:4]), 12, 31).isocalendar()[1] or
         int(s[-2:]) <= datetime.date(int(s[:4]), 12, 24).isocalendar()[1])


def __is_legal_date(year, month, day):
    try:
        d = datetime.date(year, month, day)
        return True
    except Exception as e:
        return False


def __is_day_period(s):
    """ Returns True if and only if s is a day period

    s is a date period if it is a date in the ISO date format (without a time part). Examples

    >>> is_day_period('2015-02-28')
    True

    >>> is_day_period('2015-02-31')
    False

    :param s: str
    :return:
    """

    return len(s) == 10 and \
        __is_month_period(s[:7]) and \
        s[8] in ['0', '1', '2', '3'] and \
        s[9] in __Digits and \
        0 < int(s[-2:]) <= 31 and \
        __is_legal_date(int(s[:4]), int(s[5:7]), int(s[-2:]))


def __run_tests():
    d = datetime.date.today()
    print "d = date.today()                  : {0}".format(d.isoformat())
    print "period(d,'d')                     : {0}".format(get_period(d, "d"),)
    print "period(d,'w')                     : {0}".format(get_period(d, "w"),)
    print "period(d,'m')                     : {0}".format(get_period(d, "m"),)
    print "period(d,'q')                     : {0}".format(get_period(d, "q"),)
    print "period(d,'y')                     : {0}".format(get_period(d, "y"),)
    print "quarter_num(d)                    : {0}".format(quarter_num(d),)
    print "period_start_date(d,'d')          : {0}".format(period_start_date(d, 'd').isoformat())
    print "period_end_date(d,'d')            : {0}".format(period_end_date(d, 'd').isoformat())
    print "period_start_date(d,'w')          : {0}".format(period_start_date(d, 'w').isoformat())
    print "period_end_date(d,'w')            : {0}".format(period_end_date(d, 'w').isoformat())
    print "period_start_date(d,'m')          : {0}".format(period_start_date(d, 'm').isoformat())
    print "period_end_date(d,'m')            : {0}".format(period_end_date(d, 'm').isoformat())
    print "period_start_date(d,'q')          : {0}".format(period_start_date(d, 'q').isoformat())
    print "period_end_date(d,'q')            : {0}".format(period_end_date(d, 'q').isoformat())
    print "period_start_date(d,'y')          : {0}".format(period_start_date(d, 'y').isoformat())
    print "period_end_date(d,'y')            : {0}".format(period_end_date(d, 'y').isoformat())

    print "period_start_date(d,'D')          : {0}".format(period_start_date(d, 'D').isoformat())
    print "period_end_date(d,'D')            : {0}".format(period_end_date(d, 'D').isoformat())
    print "period_start_date(d,'W')          : {0}".format(period_start_date(d, 'W').isoformat())
    print "period_end_date(d,'W')            : {0}".format(period_end_date(d, 'W').isoformat())
    print "period_start_date(d,'M')          : {0}".format(period_start_date(d, 'M').isoformat())
    print "period_end_date(d,'M')            : {0}".format(period_end_date(d, 'M').isoformat())
    print "period_start_date(d,'Q')          : {0}".format(period_start_date(d, 'Q').isoformat())
    print "period_end_date(d,'Q')            : {0}".format(period_end_date(d, 'Q').isoformat())
    print "period_start_date(d,'Y')          : {0}".format(period_start_date(d, 'Y').isoformat())
    print "period_end_date(d,'Y')            : {0}".format(period_end_date(d, 'Y').isoformat())

    print "add_months(date(2015,01,15), 1)   : {0}".format(add_months(datetime.date(year=2015, month=1, day=15), 1).isoformat())
    print "add_months(date(2015,01,31), 1)   : {0}".format(add_months(datetime.date(year=2015, month=1, day=31), 1).isoformat())
    print "add_months(date(2015,01,31), 13)  : {0}".format(add_months(datetime.date(year=2015, month=1, day=31), 13).isoformat())
    print "add_months(date(2015,01,31), -1)  : {0}".format(add_months(datetime.date(year=2015, month=1, day=31), -1).isoformat())
    print "add_months(date(2015,01,31), -13) : {0}".format(add_months(datetime.date(year=2015, month=1, day=31), -13).isoformat())

    print "period_type('2015')               : {0}".format(get_period_type('2015'))
    for i in range(0, 6):
        print "period_type('2015-Q{1}')            : {0}".format(get_period_type('2015-Q{0}'.format(i,)), i)
    for i in range(0, 14):
        print "period_type('2015-{1:02}')            : {0}".format(get_period_type('2015-{0:02}'.format(i,)), i)

    for i in range(0, 3):
        print "period_type('2015-W{1:02}')           : {0}".format(get_period_type('2015-W{0:02}'.format(i,)), i)

    for i in range(51, 55):
        print "period_type('2015-W{1:02}')           : {0}".format(get_period_type('2015-W{0:02}'.format(i,)), i)

    for i in range(0, 3):
        print "period_type('2015-01-{1:02}')         : {0}".format(get_period_type('2015-01-{0:02}'.format(i,)), i)

    for i in range(30, 33):
        print "period_type('2015-01-{1:02}')         : {0}".format(get_period_type('2015-01-{0:02}'.format(i,)), i)

    try:
        print "period_end_date(d,'X')            : {0}".format(period_end_date(d, 'X').isoformat())
    except ValueError as error:
        print error

if __name__ == "__main__":
    __run_tests()
