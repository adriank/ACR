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

from ACF.utils.xmlextras import *
from ACF.core.view import View
#from ACF.components import
from ACF.errors import *
from ACF import components,serializers
from ACF.components import *
from ACF.globals import MIMEmapper
import time,os

try:
	import simplejson
except:
	pass

D=False

class Application(object):
	appName=""
	debug=None
	lang="en"
	prefix="ACF_"
	storage=None
	immutable=False
	appDir=""
	def __init__(self,appDir):
		#cache for component objects
		self.COMPONENTS_CACHE={}
		self.DEFAULT_DB=None
		self.views={}
		self.langs=[]
		#if D: log.debug("Creating instance with appDir=%s",appDir)
		try:
			config=xml2tree(appDir+"/config.xml")
		except IOError:
			#if D: log.critical("Application config not found!")
			raise Exception("Application config not found at %s!"%(appDir+"/config.xml"))
		self.appDir=appDir
		self.config=config
		try:
			self.appName=config.get("/name/text()")[0]
		except AttributeError,e:
			#if D: log.critical("Application name not set in configuration file!")
			raise Exception("Application name not set in configuration file!")
		#for optimization we get some data from config and add it as object properties
		self.computeLangs()
		self.domain="".join(config.get("/domain/text()") or ["localhost"])
		debug=config.get("/debug")
		if debug:
			self.debug={
				"enabled":tpath(debug,"/enable/*[0]") or False,
				"level":tpath(debug,"/level/*[0]") or "error",
				"dbtimer":0,
				"dbcounter":0
			}
		self.output={
			"engine":config.get("/output[@engine]") or None,
			"xsltfile":config.get("/output[@xsltfile]") or None,
			"format":config.get("/output[@format]") or "objectml"
		}
		#engineConf=config.get("/engine")[0]
		#self.engine=te.get(engineConf[1]["name"]).engine(engineConf)
		self.prefix=(config.get("/prefix") or "ACF")+"_"
		for component in config.get("/component"):
			if D: log.debug("setting default configuration to %s component",component[1]["name"])
			self.getComponent(component[1]["name"],component[2])
		#do it or not?
		#self.config=None
		self.immutable=True

	def getDBConn(self):
		if not self.DEFAULT_DB:
			self.DEFAULT_DB=self.getComponent("database").CONNECTIONS["default"]
		return self.DEFAULT_DB

	def getComponent(self,name,conf=None):
		#print "getComponent"
		#print name
		if self.COMPONENTS_CACHE.has_key(name):
			#print "cache"
			return self.COMPONENTS_CACHE[name]
		#print "Component not in cache"
		#print components.get(name)
		o=components.get(name).getObject(conf)
		#print o
		#print "end"
		self.COMPONENTS_CACHE[name]=o
		return o

	#lazy view objects creation
	def getView(self,name):
		if self.views.has_key(name):
			view=self.views[name]
			timestamp=os.stat(view.path).st_mtime
			if timestamp<=view.timestamp:
				return view
		#print "view not in cache"
		try:
			v=View(name,self)
		except ViewNotFound, e:
			if name!="notFound":
				return self.getView("notFound")
			else:
				raise e
		self.views[name]=v
		return v

	#will be generator
	def generate(self,acenv):
		if D: t=time.time()
		prefix=acenv.prefix+"SESS"
		if acenv.cookies.has_key(prefix):
			log.info("Session cookie found")
			sessID=acenv.cookies[prefix]
			try:
				acenv.sessionStorage=FileSession(sessID)
			except:
				sessID=None
		view=self.getView(acenv.viewName)
		view.generate(acenv)
		o=Object()
		o.name="lang"
		o.current=acenv.lang
		o.supported=",".join(acenv.langs)
		acenv.generations["lang"]=o
		#temporary error handling
		try:
			s=serializers.get(globals.MIMEmapper.get(acenv.outputFormat))
		except Error, e:
			acenv.outputFormat="text/html"
			return "<html><body>"+str(e)+"</body</html>"
		if D:
			all=round((time.time()-t)*1000,5)
			dbms=round(acenv.debug["dbtimer"]*1000,5)
			print("Generated in %s"%(all))
			print("DBMS took %s"%(dbms))
			print("Python took %s"%(all-dbms))
		return s.serialize(acenv)

	def transform(self,acenv):
		self.getXML(acenv)

	def computeLangs(self):
		attrs=self.config.get("/lang")[0][1]
		try:
			self.defaultLang=attrs["default"].strip()
		except KeyError:
			#make it log.warning and fall back to en
			raise Exception("Misconfiguration of 'langs' setting in app configuration file.")
		#["","aaa"," dd   "]->["aaa","ddd"]
		self.langs=filter(len, map(str.strip, [self.defaultLang]+attrs.get("supported", "").split(",")))
		self.lang=self.langs[0]

	def __str__(self):
		return str(self.__dict__)

	def __setattr__(self, name, val):
		if self.immutable and not name=="DEFAULT_DB":
			if D: log.error("%s is read only",name)
			raise Exception("PropertyImmutable")
		self.__dict__[name]=val
