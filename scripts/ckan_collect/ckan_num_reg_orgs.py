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


def GetHDXOrganizationList():
  '''Querying the CKAN API with a specific parameter.'''


	# Querying CKAN.
  u = "https://data.hdx.rwlabs.org/api/action/organization_list"

  try:
		print "%s Connecting to HDX" % (I.item('prompt_bullet'))
		j = r.get(u).json()
		return j

  except Exception as e:
	  print "There was an error connecting to the CKAN API. Aborting." % I.item('prompt_error')
	  return False



def ProcessHDXOrgsList(json, test_data = False):
  '''Process data and store output.'''

  if json["success"] is False:
    print "%s the resulting JSON is empty. Review your HDX query and try again." % I.item('prompt_error')

  # Calculating the record. 
  if json["success"] is True:
    print "%s Processing results" % I.item('prompt_bullet')

  	##Create day-record.
    records = [{
  	  'metricid': 'ckan-number-of-orgs',
  		'period': str(time.strftime("%Y-%m-%d")),
      'period_start_date': str(time.strftime("%Y-%m-%d")),
      'period_end_date': str(time.strftime("%Y-%m-%d")),
      'period_type': 'd',
  		'value': len(json["result"])
  		}]

  	#Create week-record
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

    # Store in database.
      print "%s Generating week record." % I.item('prompt_bullet')

      record_week = {
        'metricid': 'ckan-number-of-orgs',
        'period': current_week,  # week starts at 01
        'period_start_date': first_day_of_current_week,
        'period_end_date': last_day_of_current_week,
        'period_type': 'w',
        'value': len(json["result"])
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
    json = GetHDXOrganizationList()
    ProcessHDXOrgsList(json)

    print "%s Number of organizations fetched successfully." % I.item('prompt_success')
    return True

  except Exception as e:

    if verbose is True:
      print e
      return False
    
    else:
      print "%s Failed to fetch number of organizations." % I.item('prompt_error')
      return False


def Main():
  '''Wrapper.'''
  return CollectDaily()

if __name__ == '__main__':
  CollectDaily() 