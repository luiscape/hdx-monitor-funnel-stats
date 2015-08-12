#!/usr/bin/python
# -*- coding: utf-8 -*-

from app import app
from flask import jsonify
from flask import render_template
from flask.ext.cors import cross_origin

@app.route('/')
@cross_origin()
def index():
  '''Serve the index.html file.'''
  
  return render_template('index.html')



@app.route('/status')
@cross_origin()
def statusEndpoint():
  '''Serving the status endpoint.'''
  
  s = { 
        "online": True,
        "message":"Service for tracking statistics about HDX.",
        "CKAN_instance":"https://data.hdx.rwlabs.org/",
        "version":"v.0.1.2",
        "repository":"https://github.com/luiscape/hdx-monitor-funnel-stats"
      }

  return jsonify(s)