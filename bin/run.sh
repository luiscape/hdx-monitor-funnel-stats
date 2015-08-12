#!/bin/bash

#
# Collecting the latest data.
#
source venv/bin/activate
python scripts/setup/

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
