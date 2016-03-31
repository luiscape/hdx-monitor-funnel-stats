#!/usr/bin/env python

import os
import sys

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import json
import random
import datetime
import requests
import scraperwiki

from ga_collect import datecalc
from utilities import store_records as S
from utilities import prompt_format as I


def get_metric_value(metricid, period):
    """Get the value of a metric from the database"""

    command = "value FROM funnel WHERE metricid = ? AND period = ?"
    data = scraperwiki.sql.select(command, [metricid, period])
    # print "Database being queried with: %s and %s" % (metricid, period)
    # print data
    if data:
        try:
            return float(data[0]["value"])

        except Exception as e:
            return None
    else:
        return None


def offset_period(date, period_type, offset):
    """Offset period by the number of periods periods number of period_types to period"""

    flag = period_type[0:].lower()

    if flag == datecalc.PeriodTypes.Day:
        return datecalc.get_period(date + datetime.timedelta(days=offset), period_type)
    elif flag == datecalc.PeriodTypes.Week:
        return datecalc.get_period(date + datetime.timedelta(weeks=offset), period_type)
    elif flag == datecalc.PeriodTypes.Month:
        return datecalc.get_period(datecalc.add_months(date, int(offset)), period_type)
    elif flag == datecalc.PeriodTypes.Quarter:
        return datecalc.get_period(datecalc.add_months(date, int(offset) * 3), period_type)
    elif flag == datecalc.PeriodTypes.Year:
        return datecalc.get_period(datecalc.add_months(date, int(offset) * 12), period_type)
    else:
        return None


def do_operation(operand1, operand2, operator):
    if operand1 and operand2:
        if operator == "add":
            return operand1 + operand2
        elif operator == "subtract":
            return operand1 - operand2
        elif operator == "multiply":
            return operand1 * operand2
        elif operator == "divide" and (operand2 != 0):
            return float(operand1)/float(operand2)
        else:
            return None
    else:
        return None


def calculate_funnel_data(date, period_type):

    data = []

    # Initialise values for the period and its start
    # and end dates
    period = datecalc.get_period(date, period_type)
    period_start_date = datecalc.period_start_date(date, period_type)
    period_end_date = datecalc.period_end_date(date, period_type)

    # The list of calculated metrics is stored in the database.
    # If a calculation (C2) depends on the result of another
    # calculation (C1), then C2 will have a higher calcsortorder
    # value than C1.

    calculated_metrics = scraperwiki.sql.select(
        "* FROM metrics WHERE calculated ORDER BY calcsortorder ASC")

    for metric in calculated_metrics:
        operand1 = get_metric_value(
            metric["operand1metricid"],
            offset_period(
                date,
                period_type,
                float(metric["operand1periodoffset"])
            )
        )
        operand2 = get_metric_value(
            metric["operand2metricid"],
            offset_period(
                date,
                period_type,
                float(metric["operand2periodoffset"])
            )
        )
        value = do_operation(operand1, operand2, metric["operation"])

        #
        #  Debug code.
        #
        if value is not None:
            data.append({
                "metricid": metric["metricid"],
                "period": period,
                "value": value,
                "period_type": period_type,
                "period_start_date": period_start_date.isoformat(),
                "period_end_date": period_end_date.isoformat()
                })

    S.StoreRecords(data, table = "funnel", verbose = False)
    return True


def get_initial_setup_data():
    """Calculate all data from 24 May 2014 to the current date"""

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    date = datetime.date(2014, 5, 26)
    # date = datetime.date(2016, 3, 28)

    while date < yesterday:
        calculate_funnel_data(date, 'd')
        calculate_funnel_data(date, 'w')
        calculate_funnel_data(date, 'y')

        print "%s Week of %s done." % (I.item('prompt_bullet'), date)
        date = date + datetime.timedelta(weeks=1)



if __name__ == "__main__":
    get_initial_setup_data()
