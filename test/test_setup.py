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

from mock import patch
from scripts.utilities import store_records as Store


class SWDatabaseManagementTest(unittest.TestCase):
  '''Unit tests for the ScraperWiki database management scripts.'''

  def test_database_connection(self):
    p = scraperwiki.sqlite.show_tables()
    assert type(p) == dict

  def test_database_available(self):
    tables = scraperwiki.sqlite.show_tables()
    assert 'funnel' in tables.keys()
    assert 'metrics' in tables.keys()


class StoringRecordsTest(unittest.TestCase):
  '''Unit tests for the storing records mechanism.'''
  
  def test_storing_record(self):
    data = [{ 'metricid': 'test', 'period': 'test', 'value': 4 }]
    assert Store.StoreRecords(data, table = 'funnel') == True


class DatabaseCreationTest(unittest.TestCase):
  '''Testing the process of creating a database.'''

  def test_creating_database(self):
    assert Setup.CreateTables() == True

  def test_tables_exist(self):
    tables = scraperwiki.sqlite.show_tables()
    assert 'funnel' in tables.keys()
    assert 'metrics' in tables.keys()
