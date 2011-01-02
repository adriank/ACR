#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
from wsgiref.simple_server import make_server
from wsgiref import simple_server
from ACR.backends.standalone import standalone_server
from ACR import acconfig

acconfig.appsDir="/home/adrian/projects/"
host=""
port=9999
if len(sys.argv)>1:
	port=int(sys.argv[1])
#print os.getpid()

class WSGIServer(simple_server.WSGIServer):
	request_queue_size = 500

class Handler(simple_server.WSGIRequestHandler):
	def log_message(self, *args):
		pass

#args = parser.parse_args()

httpd=WSGIServer((host,port), Handler)
httpd.set_app(standalone_server)
httpd.serve_forever()
