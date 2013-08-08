#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys,os
from wsgiref.simple_server import make_server
from wsgiref import simple_server
from ACR.backends.standalone import standalone_server
from ACR import acconfig

class WSGIServer(simple_server.WSGIServer):
	request_queue_size = 500

class Handler(simple_server.WSGIRequestHandler):
	def log_message(self, *args):
		pass

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Command line options')
	parser.add_argument('--port', type=int, help='port number')
	parser.add_argument('--host', dest='host', help='host')
	parser.add_argument('-p', '--project', dest='appDir', help='One project mode. Directory path')
	parser.add_argument('-P', '--projectsDir', dest='appsDir', help='Multiproject mode. Directory with projects path')
	parser.add_argument('-c', '--config', dest='ACRconf', help='config file')
	parser.set_defaults(port = 9999, host='', appsDir=os.path.join(os.path.expanduser('~'),"projects"), appDir='', ACRconf='')
	args = parser.parse_args()

	acconfig.appsDir = os.path.expanduser(args.appsDir)
	acconfig.ACRconf = args.ACRconf
	acconfig.appDir = os.path.expanduser(args.appDir)

	print "One-threaded server is running on %s:%s"%(args.host or "*", args.port)
	httpd = WSGIServer((args.host, args.port), Handler)
	httpd.set_app(standalone_server)
	httpd.serve_forever()
