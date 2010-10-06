#!/usr/bin/python
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

#TODO this file is mess. Need for full rewrite.

import sys,os,re,time#,logging
#logging.doLog=True
#logging.doLog=False
from ACF import globals,errors
from ACF.utils import HTTP
from ACF.core.environment import Environment
from ACF.core.application import Application
from cStringIO import StringIO
import cgi
#from guppy import hpy

#logging.basicConfig()
#log=logging.getLogger("ACF.WSGIHandler")
#logStream=StringIO()
#handler=logging.StreamHandler()#(sys.stdout)#(strm=logStream)
#handler.setFormatter(logging.Formatter('<item origin="%(name)s.%(funcName)s" line="%(lineno)d" level="%(levelname)s" file="%(filename)s"><message>%(message)s</message></item>'))
##log.addHandler(handler)
#logging.logThreads=0
#logging.logProcesses=0
#logging.logMultiprocessing=0
#log.setLevel(logging.ERROR)
APP_CACHE={}

def computeMIME(mime,agent):
	if "text/html" in mime or "*/*" in mime:
		#agent=acenv.UA
		if ((agent.find("translat")==-1) and re.search("Gecko|IE|Opera|Chrome",agent) and agent.find("Konqueror")==-1):
			return "text/xml"
		else:
			return "text/html"
	elif "application/json" in mime and len(mime)==1:
		return "application/json"

#SLOW!!!
def computePOST(env):
	post=None
	contentType=env['CONTENT_TYPE']
	if contentType.startswith("application/x-www-form-urlencoded"):
		POST=env['wsgi.input'].read()
		post=HTTP.parsePOST(POST)
	elif contentType.startswith("multipart/form-data"):
		form=cgi.FieldStorage(env['wsgi.input'],environ=env)
		post={}
		for i in form.keys():
			if type(form[i]) is list:
				l=[]
				for item in form[i]:
					l.append(item.value)
				post[i]=l
			elif form[i].filename is not None:
				post[i]={
					"filename":form[i].filename,
					"content":form[i].value
				}
			else:
				post[i]=form[i].value
	return post

def application(env,start_response):
	t=time.time()
	response=[]
	if globals.appsDir:
		path=os.path.join(globals.appsDir,env["HTTP_HOST"].split(':')[0])
	else:
		path=globals.appDir
	print path
	if APP_CACHE.has_key(path):
		app=APP_CACHE[path]
		# if application config file changes, reload whole app
		if app.checkRefresh():
			app = Application(path)
	else:
		app=Application(path)
		APP_CACHE[path]=app
	acenv=Environment(app)
	acenv.mime=map(str.strip, env["HTTP_ACCEPT"].split(";")[0].split(","))
	acenv.UA=env["HTTP_USER_AGENT"]
	acenv.output["format"]=computeMIME(acenv.mime,acenv.UA)
	#if app.debug["enabled"]:
	#	log.setLevel(globals.logLevels.get(app.debug["level"],logging.ERROR))
	if env.get('HTTP_COOKIE',None):
		acenv.cookies=HTTP.parseCookies(acenv,env['HTTP_COOKIE'])
	acenv.setLang(str(env.get("HTTP_ACCEPT_LANGUAGE","").split(",")[0].split("-")[0]))
	post=None
	if env.get('REQUEST_METHOD',"").lower()=="post":
		post=computePOST(env)
	acenv.posts=post
	acenv.URLpath=filter(lambda x: not str.isspace(x) and len(x)!=0,env['PATH_INFO'].split("/"))
	output=app.generate(acenv)
	headers=acenv.outputHeaders
	headers.append(("Content-Type",acenv.output["format"]))
	status='200 OK'
	if acenv.doRedirect:
		status="301 Redirected"
	start_response(status, headers)
	if not acenv.doRedirect:
		response.append(output)
	print round((time.time()-t)*1000,2)
	#h = hpy()
	#print h.heap()
	return response

try:
	from paste.exceptions.errormiddleware import ErrorMiddleware
	application = ErrorMiddleware(application, debug=True)
except:
	pass
