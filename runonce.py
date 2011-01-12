#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
from wsgiref.handlers import CGIHandler
from ACR.backends.WSGIHandler import application
from ACR import acconfig

#this is ugly but we need to set the absolute path so whole system knows where get files from
#TODO export settings to /etc/ACR/config
acconfig.ACRconf="/home/adrian/ACR/ACRconf.xml"
#one app run
acconfig.appDir="/home/adrian/projects/lz"
#for multiple apps run - NotImplementedYet
#globals.appsDir="/home/adrian/ACR/project/"
host=""
port=9999
#if len(sys.argv)>1:
#	port=sys.argv[1]
##print os.getpid()
#httpd=make_server(host, port, application)
#httpd.serve_forever()
try:
	os.environ["PATH_INFO"]=sys.argv[1]
except:
	print "Usage ./run.py path"
CGIHandler().run(application)
