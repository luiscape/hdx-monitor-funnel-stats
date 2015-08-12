#!/bin/bash

## Downloading the app from GitHub
## You'll need credentials ...
git clone https://github.com/luiscape/bureau
cd bureau

## Installing virual env + requirements
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
python setup.py

## Cleaning-up.
cd temp
rm *.csv