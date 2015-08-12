#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('./scripts')

from datetime import date, timedelta
from hdx_format import item
from ga_collect import ga_collect
from store_records import storeRecords
import ckan_num_reg_users as CKANUsers
import ckan_num_reg_orgs as CKANOrgs


# This should be called, not defined here.
def CollectGA(verbose = True):
  '''Collecting the latest Google Analytics data.'''
  print "%s Collecting Google Analytics data." % item('prompt_bullet')
  try: 
    records = ga_collect.get_last_weeks_data()
    print json.dumps(records)
    storeRecords(data = records, table = "funnel")
    print "%s Google Analytics collection ran successfully." % item('prompt_success')
    return True

  except Exception as e:
    if verbose:
      print e
      return False

    print "%s Google Analytics failed to run." % item('prompt_error')


def Main():
  '''Wrapper.'''
  CollectGA()
  CKANUsers.CollectDaily()
  CKANOrgs.CollectDaily()


if __name__ == "__main__":
  print "%s Running daily jobs." % item('prompt_bullet')
  Main()