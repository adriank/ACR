#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys,os
from wsgiref.simple_server import make_server
from wsgiref.handlers import CGIHandler
from ACR.backends.standalone import standalone_server
from ACR import globals
import getpass
username=getpass.getuser()
try:
	__import__(username+"_conf")
except:
	raise Exception("This is development version of ACR! You should download the ACR GA.")

#this is ugly but we need to set the absolute path so whole system knows where get files from
#TODO export settings to /etc/ACR/config
globals.ACRconf="/home/adrian/ACR/ACRconf.xml"
#one app run
globals.appDir="/home/adrian/ACR/adrian/doc/"
#for multiple apps run - NotImplementedYet
#globals.appsDir="/home/adrian/ACR/project/"
host=""
port=9999
#if len(sys.argv)>1:
#	port=sys.argv[1]
#print os.getpid()
httpd=make_server(host, port, standalone_server)
#httpd.serve_forever()
try:
	os.environ["PATH_INFO"]=sys.argv[1]
except:
	print "Usage ./run.py path"
CGIHandler().run(standalone_server)
