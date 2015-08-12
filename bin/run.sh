#!/bin/bash

#
# Collecting the latest data.
#
cd ..
python scripts/setup/

#
# Cleaning up.
#
cd temp/
rm *.csv

#
# Running server.
#
source venv/bin/activate
python wsgi.py
