#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import shutil
import requests
import scraperwiki

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

from calc_collect import calc
from ga_collect import datecalc
from ga_collect import ga_collect

from app_config import load as L
from utilities import prompt_format as I
from utilities import store_records as S
from datetime import date, timedelta, datetime

def create_tables():
    '''Creating the tables of the new database.'''

    sql_statements = {
        'funnel': 'CREATE TABLE IF NOT EXISTS funnel(metricid TEXT, period TEXT, period_start_date TEXT, period_end_date TEXT, period_type TEXT, value REAL, PRIMARY KEY(metricid,period))',
        'metrics': 'CREATE TABLE IF NOT EXISTS metrics(metricid TEXT, calculated INTEGER, name TEXT, description TEXT, operand1metricid TEXT, operand1periodoffset TEXT, operand2metricid TEXT, operand2periodoffset TEXT, operation TEXT, calcsortorder TEXT)'
        # "_log": 'CREATE TABLE IF NOT EXISTS _log(date TEXT, script TEXT, metricid TEXT, success TEXT, log_file TEXT)'
    }

    for table in sql_statements:
        try:
            query = scraperwiki.sqlite.execute(sql_statements[table])
            print "%s Table `%s` created." % (I.item('prompt_bullet'), str(table))

        except Exception as e:
            print e
            return False


    print "%s Database created successfully.\n" % I.item('prompt_success')
    return True



def sync_metrics():
    '''Sync the metrics metadata with the new database.'''

    # Download
    data_dir = os.path.split(dir)[0]
    path = os.path.join(data_dir, "temp", "metrics.csv")

    gdocs_url = "https://docs.google.com/spreadsheets/d/14kZ2Cj_IaBP1J4KZqhHTOb67HmymC5otSSV_3ji_Ssg/export?format=csv"

    r = requests.get(gdocs_url, stream = True)

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    # Read file and store in database.
    try:
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            records = []
            for row in reader:
                    records.append(row)

    except Exception as e:
        print e
        return False

    try:
        print "%s Syncing `metrics` table." % I.item('prompt_bullet')
        S.StoreRecords(records, table = "metrics")
        print "%s successfully synced `metrics` table.\n" % I.item('prompt_success')
        return True

    except Exception as e:
        print e
        print "%s failed to sync `metrics` table." % I.item('prompt_error')
        return False



def collect_previous_ga_data(verbose = False, test_data = False):
    '''Collecting historical Google Analytics data with the new database.'''

    counter = 0
    period_date = date.today()

    # Google Analytics only has data available
    # from 2014-05-25, not earlier.
    while period_date > date(2014, 5, 25):
        period_date = date.today() - timedelta(weeks=counter)
        counter += 1

        try:
            print "%s collecting data for week %s of %s" % (I.item('prompt_bullet'), period_date.isocalendar()[1], period_date.isocalendar()[0])
            records = ga_collect.collect_ga_data(period_date)
            S.StoreRecords(data = records, table = "funnel")

            if test_data is True and counter > 1:
                return records

        except Exception as e:
            if verbose:
                print e
                return False

            print "%s Google Analytics failed to run." % I.item('prompt_error')

    print "%s Google Analytics collection ran successfully." % I.item('prompt_success')
    return True



def collect_previous_ckan_data(test_data = False):
    '''Syncing historical CKAN data with the newly installed database.'''

    #
    #  TODO: This is a major failure point.
    #  This collector relies on data collected
    #  by a very old collector written in R
    #  and hosted in ScraperWiki.
    #
    data_dir = os.path.split(dir)[0]
    path = os.path.join(data_dir, "temp", "ckan_data.csv")
    u = "https://ds-ec2.scraperwiki.com/7c6jufm/bwbcvvxuynjbrx2/cgi-bin/csv/ckan_dataset_data.csv"

    r = requests.get(u, stream = True)

    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    # Read file and store in database.
    try:

        print "%s Fetching CKAN historical data." % I.item('prompt_bullet')

        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            records = []
            for row in reader:
                user = {
                    'metricid': 'ckan-number-of-users',
                    'period': row["date"],
                    'period_start_date': row["date"],
                    'period_end_date': row["date"],
                    'period_type': "d",
                    'value': row["number_of_users"]
                }
                orgs = {
                    'metricid': 'ckan-number-of-orgs',
                    'period': row["date"],
                    'period_start_date': row["date"],
                    'period_end_date': row["date"],
                    'period_type': "d",
                    'value': row["number_of_organizations"]
                }
                datasets = {
                    'metricid': 'ckan-number-of-datasets',
                    'period': row["date"],
                    'period_start_date': row["date"],
                    'period_end_date': row["date"],
                    'period_type': "d",
                    'value': row["number_of_datasets"]
                }
                records.append(user)
                records.append(orgs)
                records.append(datasets)

                record_date = datetime.strptime(row["date"], "%Y-%m-%d")
                if record_date == datecalc.period_start_date(date = record_date, period_type = "w"):
                    record_week = datecalc.get_period(date = record_date, period_type = "w")

                    #
                    #  Adding weekly records to the
                    #  record collection.
                    #
                    user["period"] = record_week
                    user["period_type"] = "w"
                    orgs["period"] = record_week
                    orgs["period_type"] = "w"
                    datasets["period"] = record_week
                    datasets["period_type"] = "w"

                    records.append(user)
                    records.append(orgs)
                    records.append(datasets)


            #
            #  Store records in database.
            #
            print "%s Storing CKAN historical data (%s records)." % (I.item('prompt_bullet'), len(records))
            S.StoreRecords(records, table = "funnel")

            if test_data:
                return records


    except Exception as e:
        print e
        return False

    print "%s Successfully collected historic CKAN records." % I.item('prompt_success')
    return True


def run_historical_calculations():
    '''Making the calculations.'''

    print "%s Making historical calculations." % I.item('prompt_bullet')

    try:
        calc.get_initial_setup_data()

    except Exception as e:
        print e

    print "%s successfully performed historical calculations.\n" % I.item('prompt_success')


def main():

    # Setting up database.
    create_tables()
    sync_metrics()

    # Collecting previous data.
    collect_previous_ga_data()
    collect_previous_ckan_data()

    # Running historic calculations.
    run_historical_calculations()


if __name__ == '__main__':
    main()
