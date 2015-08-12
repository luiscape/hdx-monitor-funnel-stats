#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import json
import time
import scraperwiki
import requests as r

from utilities import prompt_format as I
from utilities import store_records as S
from datetime import datetime, timedelta, date


def GetDatasetList():
  '''Query CKAN for a list of datasets.'''

  # Querying CKAN.
  u = "https://data.hdx.rwlabs.org/api/action/current_package_list_with_resources?limit=2000"
  headers = { 'Authorization': L.LoadConfig('dev')['hdx_key'] }

  try:
    print "%s Fetching dataset list from HDX." % (I.item('prompt_bullet'))
    j = r.get(u, headers=headers).json()
    return j

  except Exception as e:
    print "%s There was an error connecting to the CKAN API. Aborting." % I.item('prompt_error')
    return False


def CalculateMetric(json, test_data = False):
  '''Process dataset list data and store output.'''

  print "%s Calculating private datasets." % I.item('prompt_bullet')

  records = [{
    'metricid': 'ckan-number-of-private-dataset',
    'period': str(time.strftime("%Y-%m-%d")),
    'period_start_date': str(time.strftime("%Y-%m-%d")),
    'period_end_date': str(time.strftime("%Y-%m-%d")),
    'period_type': 'd',
    'value': 0
  }]

  i = 0
  for dataset in json['result']:
    if dataset['private']:
      records[0]['value'] += 1

    i += 1
    progress = round((float(i) / len(json['result'])),3) * 100
    print "%s Progress: %s%%" % (I.item('prompt_bullet'), progress)

  # Create week-record
  current_day_date = datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")
  current_week = time.strftime("%Y-W") + str(int(time.strftime('%U')) + 1)
  start = current_day_date - timedelta(days = current_day_date.weekday())
  end = start + timedelta(days = 6)
  first_day_of_current_week = start.strftime('%Y-%m-%d')
  last_day_of_current_week = end.strftime('%Y-%m-%d')

  ## Faking week data
  ## for test purposes.
  if test_data is True:
    current_day_date = last_day_of_current_week

  if current_day_date == last_day_of_current_week:

    print "%s Generating week record." % I.item('prompt_bullet')

    record_week = {
      'metricid': 'ckan-number-of-orgs',
      'period': current_week,  # week starts at 01
      'period_start_date': first_day_of_current_week,
      'period_end_date': last_day_of_current_week,
      'period_type': 'w',
      'value': records[0]['value']
    }
    records.append(record_week)
  

  S.StoreRecords(data = records, table = 'funnel')

  if test_data is True:
    return records

  else:
    return True


def CollectDaily(verbose = True):
  '''Collecting daily data.'''

  try: 
    dataset_list = GetDatasetList()
    CalculateMetric(json=dataset_list)

    print "%s Number of private datasets fetched successfully." % I.item('prompt_success')
    return True

  except Exception as e:

    if verbose is True:
      print e
      return False
    
    else:
      print "%s Failed to fetch number of private datasets." % I.item('prompt_error')
      return False

def Main():
  '''Wrapper.'''
  def CollectDaily()

if __name__ == '__main__':
  CollectDaily()