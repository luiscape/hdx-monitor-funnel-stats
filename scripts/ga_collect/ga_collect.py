__author__ = 'Godfrey Takavarasha'


import os
import time
import json
import datecalc
from httplib2 import Http
from datetime import date
from datetime import timedelta
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import SignedJwtAssertionCredentials


dir = os.path.dirname(__file__) 

def get_ga_service(client_email, private_key):
    """ Initialises a ga service object

    :param client_email: application's email address
    :param private_key: application's private key
    :return: instance of google analytics service object
    """

    service_account_name = 'https://www.googleapis.com/auth/analytics.readonly'
    credentials = SignedJwtAssertionCredentials(client_email, private_key, service_account_name)
    http = credentials.authorize(Http())
    return build('analytics', 'v3', http=http)


def get_results(service, profile_id, start_date, end_date, metrics, dimensions, filters):
    """ Gets query results from the ga service

    """

    # We will most likely encounter [Quota Error: User Rate Limit Exceeded] errors. The internet says
    # it is best to pause for a second when you encounter the error and try again. Here we implement
    # a strategy of waiting 1 seconds the first time, then 2 seconds the second time, then 3 seconds
    # the third time, after which we give up and let the error propagate through the call chain. The
    # for loop is redundant if the call to ga() succeeds since our call is a return statement.

    for sleep_duration in [1, 2, 3]:
        try:
            return service.data().ga().get(
                ids="ga:" + profile_id,
                start_date=start_date,
                end_date=end_date,
                metrics=metrics,
                dimensions=dimensions,
                filters=filters).execute()
        except HttpError as e:
            print e
            for x in e:
                print x
            time.sleep(sleep_duration)


def print_data_table(results):
    """ *** This is throw away code that prints the results from the call to ga().get()

    :param results:
    :return:
    """
    # Print headers.
    output = []
    for header in results.get('columnHeaders'):
        output.append('%30s' % header.get('name'))
        print ''.join(output)

    # Print rows.
    if results.get('rows', []):
        for row in results.get('rows'):
            output = []
            for cell in row:
                output.append('%30s' % cell)
            print ''.join(output)
    else:
        print 'No Results Found'


def get_application_email_address():
    """ Returns the email address of the application

    :return: str
    """
    base_path = os.path.split(os.path.split(dir)[0])[0]
    with open(os.path.join(base_path, 'secrets/application-email-address.txt'), 'r') as f:
        return f.read()


def get_application_private_key():
    """ Returns the private key of the application

    :return: byte
    """
    base_path = os.path.split(os.path.split(dir)[0])[0]
    with open(os.path.join(base_path, 'secrets/application-private-key.p12'), 'rb') as f:
        return f.read()


def get_ga_metrics_list():
    """ Gets the list of metrics we are interested in scraping

    :return: json: list of metrics to download from ga
    """
    with open(os.path.join(dir, 'metrics.json'), 'r') as f:
        return json.loads(f.read())['metric_list']


def get_results_value(results):
    """ Gets the value in the last column of the first row of the ga results

    :param results: dict: results from the ga analytics query
    :return: int: the value from the results
    """

    if results.get('rows', []):
        return results.get('rows')[0][-1]
    return None


def collect_period_ga_data(service, metric_def_list, period_def):
    """ Collects

    :param service: the ga service object
    :param metric_def_list: the list of metric definitions
    :param period_def: period defini
    :return: list, a list of dicts containing metric data
    """
    ga_data = []
    for metric_def in metric_def_list:
        metrics = metric_def['metrics']
        dimensions = ''
        filters = ''
        if len(metric_def['filters']) > 0:
            for filter_def in metric_def['filters']:
                dimensions += ',' + filter_def['dimension']
                if filter_def['value']:
                    filters += ';{0}=={1}'.format(filter_def['dimension'], filter_def['value'])
            dimensions = dimensions[1:]
            filters = filters[1:]

        # Send the None value to ga().get() if there are no dimensions
        if len(dimensions) == 0:
            dimensions = None

        # Send the None value to ga().get() instead of an empty string if there are no filters.
        # Sending an empty string will throw a ValueError exception
        if len(filters) == 0:
            filters = None

        #Send the query to ga()
        results = get_results(
            service=service,
            profile_id="85660823",
            start_date=period_def["period_start_date"],
            end_date=period_def["period_end_date"],
            metrics=metrics,
            dimensions=dimensions,
            filters=filters
        )

        ga_data.append({
            "metricid": metric_def['metricid'],
            "period": period_def["period"],
            "period_start_date": period_def["period_start_date"],
            "period_end_date": period_def["period_end_date"],
            "period_type": period_def["period_type"],
            "value": get_results_value(results)
        })

        # print ga_data[len(ga_data)-1]

    return ga_data


def get_all_previous_periods(base_date):
    """ Returns an array of all the previous periods that are supported

    :param base_date:
    :return:
    """
    periods = []
    for flag in datecalc.PeriodTypes.Allowed_Period_Types:
        if flag == datecalc.PeriodTypes.Day:
            prev_period = base_date + timedelta(days=-1)
        elif flag == datecalc.PeriodTypes.Week:
            prev_period = base_date + timedelta(weeks=-1)
        elif flag == datecalc.PeriodTypes.Month:
            prev_period = datecalc.add_months(base_date, -1)
        elif flag == datecalc.PeriodTypes.Quarter:
            prev_period = datecalc.add_months(base_date, -3)
        elif flag == datecalc.PeriodTypes.Year:
            prev_period = datecalc.add_months(base_date, -12)

        periods.append(
            {
                "period": datecalc.get_period(prev_period, flag),
                "period_start_date": datecalc.period_start_date(prev_period, flag).isoformat(),
                "period_end_date": datecalc.period_end_date(prev_period, flag).isoformat()
            }
        )
    return periods


def collect_ga_data(base_date):
    data = []
    metrics_list = get_ga_metrics_list()
    period_defs = [
        {
            "period": datecalc.get_period(base_date, datecalc.PeriodTypes.Week),
            "period_start_date": datecalc.period_start_date(base_date, datecalc.PeriodTypes.Week).isoformat(),
            "period_end_date": datecalc.period_end_date(base_date, datecalc.PeriodTypes.Week).isoformat(),
            "period_type": "w"
        }
    ]
    service = get_ga_service(
        client_email=get_application_email_address(),
        private_key=get_application_private_key()
    )
    for period_def in period_defs:
        period_data = collect_period_ga_data(
            service=service,
            metric_def_list=metrics_list,
            period_def=period_def
        )
        for item in period_data:
            data.append(item)
    return data


def get_last_weeks_data():
    return collect_ga_data(date.today() - timedelta(weeks=1))

def main():
    print get_last_weeks_data()


if __name__ == "__main__":
    main()