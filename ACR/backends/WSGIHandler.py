#!/usr/bin/python
# -*- coding: utf-8 -*-

# Asyncode Runtime - XML framework allowing developing internet
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

import sys,os,re,time
from ACR import acconfig, errors
from ACR.utils import HTTP
from ACR.core.environment import Environment
from ACR.core.application import Application
from cStringIO import StringIO
#try:
#	from guppy import hpy
#except:
#	pass

APP_CACHE={}

def computeMIME(mime,agent):
	return "application/json"
	# if not agent:
	# 	return mime[0]
	# if "text/html" in mime or "*/*" in mime:
	# 	if ((agent.find("translat")==-1) and re.search("Firefox|IE|Opera|Chrome",agent) and agent.find("Konqueror")==-1 and agent.find("rekonq")==-1):
	# 		return "application/xml"
	# 	else:
	# 		return "text/html"
	# elif "application/json" in mime and len(mime)==1:
	# 	return "application/json"
	# return mime[0]

def application(env,start_response):
	#for i in env:
	#	print i+": "+str(env[i])
	t=time.time()
	response=[]
	D=acconfig.debug
	path=env["HTTP_HOST"]
	if APP_CACHE.has_key(path):
		app=APP_CACHE[path]
		# if application config file changes, reload whole app
		#D=app.dbg.get("enabled",False)
		if not app.deploymentMode and not app.isUpToDate():
			app=Application(path)
	else:
		app=Application(path)
		APP_CACHE[path]=app
	acenv=Environment(app)
	D=acenv.doDebug
	acenv.env["clientIP"]=env.get("REMOTE_ADDR","unknown")
	acenv.mime=map(str.strip, env.get("HTTP_ACCEPT","application/xml").split(";",1)[0].split(","))
	acenv.UA=acenv.env["UA"]=env.get("HTTP_USER_AGENT")
	if D:
		acenv.debug("MIME is: %s",acenv.mime)
		acenv.debug("UA is: %s",acenv.UA)
	acenv.output["format"]=computeMIME(acenv.mime,acenv.UA)
	if D: acenv.debug("Computed output format is: %s",acenv.output["format"])
	if env.get('HTTP_COOKIE'):
		acenv.cookies=acenv.env["cookies"]=HTTP.parseCookies(acenv,env['HTTP_COOKIE'])
	acenv.setLang(str(env.get("HTTP_ACCEPT_LANGUAGE","").split(",",1)[0].split("-",1)[0]))
	post=None
	if env.get('REQUEST_METHOD',"").lower()=="post":
		post=HTTP.computePOST(env)
	acenv.posts=post
	strisspace=str.isspace
	acenv.URLpath=filter(lambda x: len(x)!=0 or strisspace(x), env['PATH_INFO'].split("/"))
	output=app.generate(acenv)
	headers=acenv.outputHeaders
	headers.append(("Content-Type",acenv.output["format"]))
	status='200 OK'
	if acenv.doRedirect:
		status="303 See other"
	start_response(status, headers)
	if acenv.doRedirect:
		response.append("")
	else:
		response.append(output)
	if acenv.doProfiling:
		whole=round((time.time()-t)*1000,2)
		headerstime=whole-acenv.profiler["alltime"]
		print("Time spent on parsing HTTP headers and building objects: %sms"%(headerstime))
		print("Time spent on Python and waitings: %sms"%(headerstime+acenv.profiler["pytime"]))
		print "Request satisfied in %sms"%whole
		print "WARNING! Python time includes some waitings related to one-threaded nature of WSGIRef. These waitings are not existent in deployment instalations due to multiprocessing/threading/asynchrony, but are stable through multiple runs. Use above timings to optimize your views. Measure time of 'HelloWorld!' app and substract the values from the results.\nRun the tests multiple times and get the mean to get best results!"
	#h = hpy()
	#print h.heap()
	return response

try:
	from paste.exceptions.errormiddleware import ErrorMiddleware
	application=ErrorMiddleware(application, debug=True)
except:
	pass
