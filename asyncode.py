#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
from wsgiref.simple_server import make_server
from wsgiref import simple_server
#from wsgiref.handlers import CGIHandler
from ACF.backends.standalone import standalone_server
from ACF import globals
#import getpass
#import cProfile

#username=getpass.getuser()
#print username
#username=getpass.getuser()
#try:
#	__import__(username+"_conf")
#except:
#	raise Exception("This is development version of ACF! You should download the ACF GA.")
#sys.argv[0] = 'acf'
#try:
#	globals.dirs=filter(os.path.isdir, map(lambda f: os.path.join(globals.appsDir,f),os.listdir(globals.appsDir)))
#except:
#	pass
#this is ugly but we need to set the absolute path so whole system knows where get files from
#TODO export settings to /etc/ACF/config
#globals.ACFconf="/home/adrian/ACF/ACFconf.xml"
#one app run
#globals.appDir="/home/adrian/ACF/adrian/doc/"
#for multiple apps run - NotImplementedYet
globals.appsDir="/home/adrian/ACF/project/"
host=""
port=9999
if len(sys.argv)>1:
	port=int(sys.argv[1])
print os.getpid()

class PimpedWSGIServer(simple_server.WSGIServer):
	request_queue_size = 500

class PimpedHandler(simple_server.WSGIRequestHandler):
	def log_message(self, *args):
		pass

httpd = PimpedWSGIServer((host,port), PimpedHandler)
httpd.set_app(standalone_server)
#cProfile.run('httpd.serve_forever()')
httpd.serve_forever()
