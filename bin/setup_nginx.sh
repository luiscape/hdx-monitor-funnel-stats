#!/bin/bash

## Config
SCRIPTS_PATH="scripts"

## Making the terminal more welcoming.
export PS1="digital-\[\e[01;36m\]\u\[\e[0m\]\[\e[00;37m\] : \W \\$ \[\e[0m\]"

## Installing utilities
sudo apt-get update
apt-get install python-virtualenv
apt-get install screen
apt-get install tree
apt-get install git

## Installing NGINX
sudo apt-get install nginx

## Installing Python dependencies.
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt