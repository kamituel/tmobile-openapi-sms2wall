#!/usr/bin/env python

import re
import os
import urllib
import random
from time import sleep
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import util, template
from django.utils import simplejson as json
import logging
import email
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.mail import send_mail
import base64
import string
import cgi

# TODO: update this address with your current AppEngine app's URL
self_addr = "http://sms2walldemo.appspot.com/facebook?t=t&msisdn=%s"

# TODO: put Facebook app's credentials here
fcb_appid = ""
fcb_secret = ""

class Client (db.Model):
	msisdn = db.StringProperty()
	facebook_token = db.StringProperty()
