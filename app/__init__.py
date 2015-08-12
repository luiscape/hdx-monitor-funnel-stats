#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.cors import CORS

app = Flask(__name__)
cors = CORS(app)
from app import views