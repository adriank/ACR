#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
from wsgiref.handlers import CGIHandler
from ACR.backends.WSGIHandler import application
from ACR import acconfig
import argparse

if __name__=="__main__":
	parser=argparse.ArgumentParser(description='Command line options')
	parser.add_argument('PATH', help='path')
	parser.add_argument('-o','--output-format', dest='HTTP_ACCEPT', help='output format')
	parser.add_argument('-p', '--project', dest='appDir', help='Path to project.')
	parser.set_defaults(
		appDir=os.path.join(os.path.expanduser('~'),"projects","localhost"),
		HTTP_ACCEPT='application/json'
	)
	args = parser.parse_args()
print args
acconfig.appDir=args.appDir
host=""
port=9999
os.environ["HTTP_ACCEPT"]=args.HTTP_ACCEPT
try:
	os.environ["PATH_INFO"]=sys.argv[1]
except:
	print "Usage ./run.py path"
CGIHandler().run(application)
print
