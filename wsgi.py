#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json

import scripts
import logging

from app import app
from flask.ext.cors import CORS
from tornado.ioloop import IOLoop
from sandman.model import activate
from sandman import app as application
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from werkzeug.wsgi import DispatcherMiddleware
from scripts.utilities import prompt_format as I


## Configuration.
root = logging.getLogger()
ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.WARNING)
root.addHandler(ch)

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///scraperwiki.sqlite'
application.config['SANDMAN_GENERATE_PKS'] = True


def CheckOpenShift():
  '''Checking if the application is on an OpenShift environment.'''
  
  try:
    if os.environ['OPENSHIFT_REPO_DIR']:
      print "%s Application on OpenShift." % I.item('prompt_bullet')
      l = {
        "ip": os.environ['OPENSHIFT_PYTHON_IP'],
        "port": int(os.environ['OPENSHIFT_PYTHON_PORT'])
      }

  except Exception as e:
    print "%s Application not on OpenShift." % I.item('prompt_bullet')
    l = {
      "ip": '0.0.0.0',
      "port": 7000
    } 

  return l


def WelcomeMessage(port):
  '''Welcome.'''
  print "%s server started on port %s." % (I.item('prompt_bullet'), port)


def Main():
  '''Wrapper.'''
  v = CheckOpenShift()
  activate(browser=False, admin=False)
  application.debug = True
  WelcomeMessage(v['port'])
  http_server = HTTPServer(WSGIContainer(application))
  http_server.listen(v['port'], v['ip'])
  IOLoop.instance().start()



# Allowing CORS.
cors = CORS(application)
application = DispatcherMiddleware(app, {
    '/api': application
    })


if __name__ == "__main__":
  Main()
