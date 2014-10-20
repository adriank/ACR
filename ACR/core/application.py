#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Asyncode Runtime - XML framework allowing developing internet
# applications without using programming languages.
# Copyright (C) 2008-2010  Adrian Kalbarczyk, Marcin Radecki

# This program is free software: you can redistribute it and/or modify
# it under the terms of the version 3 of GNU General Public License as published by
# the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#@marcin: views subdirs implementation

from ACR.utils.xmlextras import *
from ACR.utils import dicttree, json_compat, str2obj
try:
	from ACR.session.mongoSession import MongoSession as sessionBackend
except:
	from ACR.session.file import FileSession as sessionBackend
from ACR.core.view import View
from ACR.errors import *
from ACR import components, serializers
from ACR.components import *
from ACR.acconfig import *
import time, os
import locale
try:
	import pymongo
except:
	print "No MongoDB driver found. Please install pymongo."

pjoin=os.path.join
pexists=os.path.exists
pisdir=os.path.isdir

class Application(object):
	appName=""
	dbg=None
	prefix="ACR_"
	storage=None
	appStorage=None
	appDir=""
	lang="en"
	immutable=False
	deploymentMode=False
	domain=""

	def __init__(self,domain):
		self.domain=domain
		domainWOPort=domain.split(':',1)[0]
		if acconfig.appDir:
			appDir=acconfig.appDir
		else:
			appDir=os.path.join(acconfig.appsDir,domainWOPort)
		#if D: log.debug("Creating instance with appDir=%s",appDir)
		self.configPath=os.path.join(appDir, "config.xml")
		try:
			if not self.deploymentMode:
				self.timestamp=os.stat(self.configPath).st_mtime
			config=xml2tree(self.configPath)
		except (IOError,OSError):
			raise AppNotFound(appDir)
		self.immutable=False
		#cache for component objects
		self.COMPONENTS_CACHE={}
		self.DEFAULT_DB=None
		self.views={}
		self.lang="en"
		self.langs=[]
		self.viewsPath=os.path.join(appDir, "")
		self.appDir=appDir
		self.config=config
		try:
			self.appName=config.get("/name/text()")[0]
		except AttributeError,e:
			#if D: log.critical("Application name not set in configuration file!")
			raise Exception("Application name not set in configuration file!")
		#for optimization we get some data from config and add it as object properties
		self.computeLangs()
		self.domain=domain#"".join(config.get("/domain/text()", ["localhost"]))
		self.DB_NAME=domainWOPort.replace(".","_")
		db_overwritten=config.get("/mongo[@db]")
		if db_overwritten:
			self.DB_NAME=db_overwritten
		connopts={}
		host=config.get("/mongo[@host]")
		if host:
			connopts["host"]=host
		if str2obj(config.get("/deployment[@enable]","f")):
			self.deploymentMode=True
		try:
			self.storage=pymongo.Connection(**connopts)[self.DB_NAME]
		except Exception,e:
			raise Error("MongoError",str(e))
		if acconfig.debug or config.get("/debug"):
			self.dbg={
				"enabled": acconfig.debug or str2obj(config.get("/debug[@enable]")),
				"level": config.get("/debug[@level]","error")
			}
		if config.get("/debug[@cutAfter]"):
			self.dbg["cutAfter"]=config.get("/debug[@cutAfter]")

		if config.get("/profiler"):
			self.profiler={
				"enabled":str2obj(config.get("/profiler[@enable]")),
				"dbtimer":0,
				"dbcounter":0
			}
		self.output={
			"XSLTFile":config.get("/output[@XSLTFile]","index.xsl"),
			"format":config.get("/output[@format]","application/xml")
		}
		forceReload=config.get("/output[@XSLTForceReload]")
		if forceReload:
			self.output["XSLTForceReload"]=str2obj(forceReload)
		self.prefix=(config.get("/prefix") or "ACR")+"_"
		for component in config.get("/component"):
			#if D: log.debug("setting default configuration to %s component",component[1]["name"])
			self.getComponent(component[1]["name"],component[2])
		#XXX do it or not?
		#self.config=None
		self.immutable=True

	# checks if an application instance should be reloaded
	def isUpToDate(self):
		return self.timestamp >= os.stat(self.configPath).st_mtime

	def getDBConn(self):
		if not self.DEFAULT_DB:
			self.DEFAULT_DB=self.getComponent("database").CONNECTIONS["default"]
		return self.DEFAULT_DB

	def getComponent(self,name,conf=None):
		if self.COMPONENTS_CACHE.has_key(name):
			return self.COMPONENTS_CACHE[name]
		o=components.get(name).getObject(conf)
		self.COMPONENTS_CACHE[name]=o
		return o

	#lazy view objects creation
	def getView(self,URLpath,errorOnNotFound=False):
		#TODO rewrite it:
		# 1. View.isUpToDate - should posibly update object internally,
		#    when view file is deleted, should raise error
		# 2. here should be try to FileNotFound error which should refresh cache
		# 3. then check for mistakes (eg. now some views are not cached)
		(o, i)=dicttree.get(self.views, URLpath, False)
		if i==len(URLpath) and type(o) is dict and o.has_key("default"):
			o=o["default"]
			#if D: acenv.debug("Executing '%s'/default"%("/".join(URLpath)))
		#TODO handle an event when file was deleted; probably raises exception
		if type(o) is View:
			if self.deploymentMode or o.isUpToDate():
				#if D: acenv.info("View '%s' taken from cache"%("/".join(URLpath[:i])))
				return (o, URLpath[i:])
		#elif D: acenv.info("View %s is not cached","/".join(URLpath))
		i=0
		viewPath=pjoin(self.viewsPath, *URLpath[:i])
		#if D: acenv.debug("Searching from '%s'"%(viewPath))
		viewName,inputs=URLpath[:i],URLpath[i:]
		temp=viewPath
#		if inputs[1]!="api"
#			raise Exception(inputs)
		while len(inputs):
			temp=pjoin(temp, inputs[0])
			if not pisdir(temp):
				break
			viewPath=temp
			viewName.append(inputs.pop(0))
		if inputs and pexists(pjoin(viewPath,inputs[0])+".xml"):
			viewName.append(inputs.pop(0))
		elif not inputs and pexists(viewPath+".xml"):
			pass
		elif not inputs and pexists(pjoin(viewPath,"default.xml")):
			viewName.append("default")
		else:
			if errorOnNotFound:
				raise ViewNotFound(viewName)
			viewName=["notFound"]
		v=View(viewName, self)
		dicttree.set(self.views, viewName, v)
		return (v, inputs)

	#will be generator
	def generate(self,acenv):
		D=acenv.doDebug
		P=acenv.doProfiling
		if D: acenv.info("START")
		if P: t=time.time()
		prefix=acenv.prefix+"SESS"
		if acenv.cookies.has_key(prefix):
			if D:acenv.info("Session cookie found")
			sessID=acenv.cookies[prefix]
			try:
				acenv.sessionStorage=sessionBackend(acenv,sessID)
			except IndexError:
				sessID=None
		try:
			if D: acenv.debug("Inputs are '%s'",acenv.inputs)
			view, acenv.inputs=self.getView(acenv.URLpath)
			view.generate(acenv)
		except Error,e:
			acenv.generations={
				"GlobalError":{
					"error":e.name,
					"message":e
				}
			}
			#FIXME - what is this for???
			try:
				acenv.output["XSLTFile"]=view.output.get("XSLTFile","error.xsl")
			except:
				pass
		acenv.generations["_acr"]["lang"]={"current":acenv.lang,"available":acenv.langs}
		acenv.generations["_acr"]["appDetails"]={"domain":acenv.domain,"config":acenv.outputConfig}
		try:
			acenv.generations["_acr"]["view"]={"path":view.name.replace(".","/")}
		except:
			pass
		if acenv.sessionStorage:
			acenv.info("Session exists")
			sess=acenv.sessionStorage.data
			acenv.generations["_acr"]["user"]={"ID":sess["ID"], "email":sess["email"],"role":sess["role"]}
			acenv.sessionStorage.save()
		try:
			s=serializers.get(acconfig.MIMEmapper.get(acenv.output["format"],"json"))
		except Error, e:
			#XXX this is wrong answer e.g. in JSON output format mode - move it to each serializer!
			acenv.output["format"]="text/html"
			return "<html><body>"+str(e)+"</body</html>"
		if P:
			all=round((time.time()-t)*1000,5)
			dbms=round(acenv.profiler["dbtimer"]*1000,5)
			dbcounter=acenv.profiler["dbcounter"]
			print("Tree generated in %sms, where:"%(all))
			if dbcounter:
				print("	DBMS took %sms in #%s queries averaging at %sms per query"%(dbms,dbcounter,dbms/dbcounter))
			else:
				print("DBMS was not used.")
			pytime=all-dbms
			print("	Python took %sms"%(pytime))
			t=time.time()
		x=s.serialize(acenv)
		if P:
			serializerTime=round((time.time()-t)*1000,5)
			acenv.profiler["pytime"]=pytime+serializerTime
			acenv.profiler["alltime"]=all+serializerTime
			print "%s serializer took\n	%sms"%(s.name,serializerTime)
			print("Asyncode Runtime took %s"%(acenv.profiler["pytime"]))
		if D: acenv.end("")
		return x

	def computeLangs(self):
		attrs=self.config.get("/lang")[0][1]
		try:
			defaultLang=attrs["default"].strip()
		except KeyError:
			raise Error("LangNotDefined","Misconfiguration of 'langs' setting in app configuration file.")
		#["","aaa"," dd   "]->["aaa","ddd"]
		self.langs=filter(len, map(str.strip, [defaultLang]+attrs.get("supported", "").split(",")))
		self.lang=self.langs[0]
		try:
			locale.setlocale(locale.LC_ALL, locale.normalize(self.lang+".UTF8"))
		except:
			locale.setlocale(locale.LC_ALL)

	def __str__(self):
		return str(self.__dict__)

	def __setattr__(self, name, val):
		if self.immutable and not name=="DEFAULT_DB":
			#if D: log.error("%s is read only",name)
			raise Exception("PropertyImmutable")
		self.__dict__[name]=val
