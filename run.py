#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys,os
from wsgiref.simple_server import make_server
from wsgiref.handlers import CGIHandler
from ACF.backends.standalone import standalone_server
from ACF import globals

#this is ugly but we need to set the absolute path so whole system knows where get files from
#TODO export settings to /etc/ACF/config
globals.ACFconf="/home/adrian/ACF/ACFconf.xml"
#one app run
globals.appDir="/home/adrian/ACFmain/doc/"
#for multiple apps run - NotImplementedYet
#globals.appsDir="/home/adrian/ACF/project/"
host=""
port=9999
if len(sys.argv)>1:
	port=sys.argv[1]
print os.getpid()
httpd=make_server(host, port, standalone_server)
#httpd.serve_forever()
os.environ["PATH_INFO"]="/"
CGIHandler().run(standalone_server)
