#!/bin/bash

#
# Collecting the latest data.
#
source venv/bin/activate
cd hdx-monitor-funnel-stats
python hdx-monitor-funnel-stats/scripts/setup/

#
# Cleaning up.
#
cd temp/
rm *.csv

#
# Running server.
#
cd ..
python wsgi.py
