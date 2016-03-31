#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from datetime import date, timedelta
from scripts.ga_collect import ga_collect
from scripts.utilities.prompt_format import item
from scripts.utilities.store_records import StoreRecords

import scripts.ckan_collect.ckan_num_reg_users as CKANUsers
import scripts.ckan_collect.ckan_num_reg_orgs as CKANOrgs


# This should be called, not defined here.
def collect_ga(verbose = True):
    '''Collecting the latest Google Analytics data.'''
    print "%s Collecting Google Analytics data." % item('prompt_bullet')
    try:
        records = ga_collect.get_last_weeks_data()
        # print json.dumps(records)
        StoreRecords(data = records, table = "funnel")
        print "%s Google Analytics collection ran successfully." % item('prompt_success')
        return True

    except Exception as e:
        if verbose:
            print e
            return False

    print "%s Google Analytics failed to run." % item('prompt_error')


def main():
  '''Wrapper.'''
  collect_ga()
  CKANUsers.CollectDaily()
  CKANOrgs.CollectDaily()


if __name__ == "__main__":
  print "%s Running daily jobs." % item('prompt_bullet')
  main()
