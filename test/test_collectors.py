#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

# Below as a helper for namespaces.
# Looks like a horrible hack.
dir = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(dir)

import mock
import unittest
import scraperwiki
import setup as Setup
from scripts.ckan_collect import ckan_num_reg_users as Users
from mock import patch

class CKANRegisteredUsersTest(unittest.TestCase):
  '''Unit tests for the CKAN registered users scraper.'''


  def test_run_program(self):
    assert Users.Main() == True

  def test_fetching_of_data(self):
    d = Users.GetHDXUserList()
    assert d != False

  def test_number_of_records(self):
    d = Users.GetHDXUserList()
    p = Users.ProcessHDXUserList(d, test_data = True)
    assert len(p) <= 2
    for record in p:
      assert len(record) == 6

  def test_for_right_record_keys(self):
    d = Users.GetHDXUserList()
    data = Users.ProcessHDXUserList(json = d, test_data = True)
    for record in data:
      assert 'metricid' in record.keys()
      assert 'period' in record.keys()
      assert 'value' in record.keys()

  def test_correct_metric_id(self):
    d = Users.GetHDXUserList()
    data = Users.ProcessHDXUserList(json = d, test_data = True)
    for record in data:
      assert record["metricid"] == 'ckan-number-of-users'

  def test_object_type_of_records(self):
    d = Users.GetHDXUserList()
    data = Users.ProcessHDXUserList(json = d, test_data = True)
    for record in data:
      assert type(record["metricid"]) == str
      assert type(record["period"]) == str
      assert type(record["value"]) == int



class SyncingGADataTest(unittest.TestCase):
  '''Testing the process of syncing Google Analytics historical data.'''

  #
  # Monkey-patch this function. Takes too long ...
  #
  def test_that_function_of_collecting_GA_data_runs(self):
    assert Setup.CollectPreviousGAData() == True

  def test_number_records_GA_historical_data(self):
    records = Setup.CollectPreviousGAData(test_data = True)
    assert len(records) > 1

  def test_records_from_collecting_GA_historical_data(self):
    records = Setup.CollectPreviousGAData(test_data = True)
    for record in records:
      assert 'metricid' in record.keys()
      assert 'period' in record.keys()
      assert 'value' in record.keys()


class SyncingCKANDataTest(unittest.TestCase):
  '''Testing the process of testing CKAN data.'''

  def test_that_function_of_collecting_CKAN_data_works(self):
    assert Setup.CollectPreviousCKANData() == True

  def test_number_of_records_CKAN_historical_data(self):
    records = Setup.CollectPreviousCKANData(test_data = True)
    assert len(records) > 1

  def test_number_of_records_CKAN_historical_data(self):
    records = Setup.CollectPreviousCKANData(test_data = True)
    for record in records:
      assert 'metricid' in record.keys()
      assert 'period' in record.keys()
      assert 'value' in record.keys()

