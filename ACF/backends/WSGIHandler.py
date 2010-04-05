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

import sys,os,re,time,logging
logging.doLog=True
logging.doLog=False
from ACF import globals,errors
from ACF.utils import HTTP
from ACF.core import Environment
from ACF.core.application import Application
from cStringIO import StringIO
import cgi
logging.basicConfig()
log=logging.getLogger("ACF.WSGIHandler")
logStream=StringIO()
handler=logging.StreamHandler()#(sys.stdout)#(strm=logStream)
handler.setFormatter(logging.Formatter('<item origin="%(name)s.%(funcName)s" line="%(lineno)d" level="%(levelname)s" file="%(filename)s"><message>%(message)s</message></item>'))
#log.addHandler(handler)
logging.logThreads=0
logging.logProcesses=0
logging.logMultiprocessing=0
log.setLevel(logging.ERROR)
APP_CACHE={}

def application(env,start_response):
	t=time.time()
	response=[]
	if globals.appsDir:
		path=os.path.join(globals.appsDir,env["HTTP_HOST"].split(':')[0])
	else:
		path=globals.appDir
	if APP_CACHE.has_key(path):
		app=APP_CACHE[path]
	else:
		app=Application(path)
		APP_CACHE[path]=app
	acenv=Environment(app)
	if app.debug["enabled"]:
		log.setLevel(globals.logLevels.get(app.debug["level"],logging.ERROR))
	if env.get('HTTP_COOKIE',None):
		acenv.cookies=HTTP.parseCookies(acenv,env['HTTP_COOKIE'])
	acenv.setLang(str(env.get("HTTP_ACCEPT_LANGUAGE","").split(",")[0].split("-")[0]))
	post=None
	##if acenv.debug:
	##	POST=""
	##	XSLTtime=None
	if env.get('REQUEST_METHOD',"").lower()=="post":
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
	acenv.posts=post
	if env.has_key('PATH_INFO'):
		acenv.viewName, acenv.inputs=HTTP.parseURL(env['PATH_INFO'].decode("utf-8"))
	else:
		acenv.viewName="default"
	print acenv.inputs
	xml=app.generate(acenv)
	headers=acenv.outputHeaders
	headers.append(("Content-Type","application/xml"))
	status='200 OK'
	if acenv.doRedirect:
		status="301 Redirected"
	start_response(status, headers)
	#print round((time.time()-t)*1000,2)
	if not acenv.doRedirect:
		response.append(xml.encode("utf-8"))
	return response

	#if acenv.debug:
	#	dbg=[]
	#	timer=round((time.time()-t)*1000,2)
	#	dbg.append("<div style=\"background:black;color:white;\">")
	#	dbg.append("Time spent on page generation: "+str(timer)+"ms<br/>")
		# this is not working because it should be added after transformation - do $$$XSLT$$$ here and str.replace after transformation?
		#if XSLTtime:
		#	dbg.append(str(XSLTtime)+"ms was spent on XSLT, which is "+str(round(100*XSLTtime/timer))+"%<br/>")
		#dbg.append("database "+str(round(globals.request.dbtimer*1000,2))+", which is "+str(round(100*globals.request.dbtimer/timer))+"%<br/>")
		#dbg.append("python "+str(timer-round(globals.request.dbtimer*1000,2))+"<br/>")
		#dbg.append("there was "+str(globals.request.dbcounter)+" queries.<br/>")
		#if globals.session is not None:
			#dbg.append("Session data: "+str(globals.session.data)+"<br/>")
		#dbg.append("POST data: <br/>")
		#if post:
		#	for i in post:
		#		dbg.append(i+": "+str(post[i])+"<br/>")
		#else:
		#	dbg.append("no POST data<br/>")
		#dbg.append("HTTP headers: <br/>"+str(env).replace("<","")+"<br/>")
		#dbg.append("Lang: "+globals.lang+"<br/>")
		#dbg.append("Other data: <br/>")
		#dbg.append(globals.request.debugString.encode("utf-8")+"<br/>")
		#dbg.append("</div>")
		#view.tree[2].append(("debug",None,[("info",None,"".join(dbg)),("executionLog",None,logStream.getvalue())]))
	#if not acenv.redirect:
	#	if acenv.output=="json":
	#		#provide application/json if HTTP accept has it
	#		acenv.outputHeaders.append(("Content-Type","application/javascript"))
	#		response.append(view.getJSON())
	#	else:
	#		xml=view.getXML()
	#		if acenv.output.lower()!="html" and ((env["HTTP_USER_AGENT"].find("translat")==-1) and re.search("Gecko|IE|Opera|Chrome",env["HTTP_USER_AGENT"]) and env["HTTP_USER_AGENT"].find("KHTML")==-1):
	#			acenv.headers.append(("Content-Type","application/xml"))
	#			s=xml.encode("utf-8")
	#			response.append(s)
	#		else:
	#			acenv.outputHeaders.append(("Content-Type","text/html"))
	#			if acenv.debug:
	#				XSLTtimestart=time.time()
	#			response.append(transform(xml.encode("utf-8"), globals.appStaticDir+"xslt/"+globals.xsltFile))
	#			if acenv.debug:
	#				XSLTtime=round((time.time()-XSLTtimestart)*1000,2)
	#
	#status='200 OK'
	#if acenv.redirect:
	#	status="302 REDIRECT"
	#length=0
	#for i in response:
	#	length+=lherpesen(i)
	#globals.request.headers.append(("Content-Length",str(length)))
	#start_response(status, globals.request.headers)
	#if not acenv.redirect:
	#	return response
	#else:
	#	return []
try:
	from paste.exceptions.errormiddleware import ErrorMiddleware
	application = ErrorMiddleware(application, debug=True)
except:
	pass
