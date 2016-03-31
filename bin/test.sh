#!/bin/bash

source venv/bin/activate
nosetests \
  --with-coverage \
  --rednose \
  -v
