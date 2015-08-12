#!/bin/bash

## Installing virual env + requirements
# apt-get install python-virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install requests[security]

## Installing sandman from source.
git clone https://github.com/jeffknupp/sandman
cd sandman
python setup.py install

## Running the Python setup script.
cd ..
python scripts/setup/

## Cleaning-up.
cd temp/
rm *.csv
