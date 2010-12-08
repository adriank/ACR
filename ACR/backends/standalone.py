#!/usr/bin/env python
# -*- coding: utf-8 -*-

# AsynCode Framework - XML framework allowing developing internet
# applications without using programming languages.
# Copyright (C) 2008-2010  Adrian Kalbarczyk

# This program is free software: you can redistribute it and/or modify
# it under the terms of the version 3 of GNU General Public License as published by
# the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import re
import os
import mimetypes
from ACF.backends.WSGIHandler import application
from ACF import globals
from ACF.utils.xmlextras import xml2tree

def r(s):
	raise Exception(s)

def serve_static(env,start_response):
	response=[]
	length=0
	status="200 OK"
	extension=env["PATH_INFO"].split(".").pop()
	if globals.appDir:
		path=globals.appDir
	else:
		path=os.path.join(globals.appsDir,env["HTTP_HOST"].split(":")[0])
	try:
		config=xml2tree(os.path.join(path,"config.xml"))
	except IOError:
		logging.critical("Application config not found!")
		raise Exception("Application config not found!")
	staticDir=os.path.join(path,"static")
	try:
		f=open(os.path.join(staticDir,*env["PATH_INFO"].split("/")))
	except:
		status="404 Not Found"
		extension="html"
		f=open(os.path.join(staticDir,"errorpages","404.html"))
	try:
		for line in f:
			response.append(line)
			length+=len(line)
	finally:
		f.close()
	headers=[
		('Content-type', mimetypes.types_map['.'+extension]),
		("Content-Length", str(length))
	]
	start_response(status,headers)
	return response

def standalone_server(env,start_response):
	try:
		extension=env["PATH_INFO"].split(".").pop()
	except Exception,e:
		pass
	else:
		if extension=="ico" or (len(extension)<5 and mimetypes.types_map.get('.'+extension,"ERROR") !='ERROR'):
		#log.debug("A static file request")
			return serve_static(env,start_response)
	#headers=[
	#	('Content-type', mimetypes.types_map['.html'])
	#]
	#start_response("200 OK",headers)
	#return ["sss"]
	return application(env, start_response)
