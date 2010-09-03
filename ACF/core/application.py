#!/usr/bin/env python
# -*- coding: utf-8 -*-

# AsynCode Framework - XML framework allowing developing internet
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

#@marcin: getView, checkRefresh, cacheView, findCachedView, findViewFile


from ACF.utils.xmlextras import *
from ACF.core.view import View
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
	prefix="ACF_"
	storage=None
	appDir=""
	lang="en"
	immutable=False
	def __init__(self,appDir):
		#cache for component objects
		self.immutable=False
		self.COMPONENTS_CACHE={}
		self.DEFAULT_DB=None
		self.views={}
		self.lang="en"
		self.langs=[]
		#if D: log.debug("Creating instance with appDir=%s",appDir)
		try:
			self.configPath = os.path.join(appDir, "config.xml")
			self.timestamp=os.stat(self.configPath).st_mtime
			config=xml2tree(self.configPath)
		except IOError:
			#if D: log.critical("Application config not found!")
			raise Exception("Application config not found at %s!"%(appDir+"\config.xml"))
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
			#if D: log.debug("setting default configuration to %s component",component[1]["name"])
			self.getComponent(component[1]["name"],component[2])
		#do it or not?
		#self.config=None
		self.immutable=True

	# checks if an application instance should be reloaded
	def checkRefresh(self):
		if self.timestamp < os.stat(self.configPath).st_mtime:
			return True
		return False

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

	#caches a view
	def cacheView(self, path, view):
		d = self.views
		for s in path[:-1]:  # without last element
			if not d.has_key(s):
				d[s] = {}
			d = d[s]
		d[path[-1]] = view # path[-1] means last element of the list

	# finds view in cache by url; return View or None, if not found
	def findCachedView(self, URLpath):
		tempPath = []
		d = self.views
		v = None
		for s in URLpath[:]:
			tempPath.append(URLpath.pop(0))
			if d.has_key(s):
				if type(d[s]) != dict:
					v = d[s]
					break
				d = d[s]
				if not URLpath: # last loop
					if d.has_key('default'):
						tempPath.append('default')
						v = d['default']
			else:
				break
		if v:
			timestamp = os.stat(v.path).st_mtime
			if timestamp <= v.timestamp:
				return (v, tempPath, URLpath)
		return None

	# finds view file stored on hdd. Seperate view path from inputs.
	# Algorithm is greedy, so it finds first view which suits url.
	def findViewFile(self, URLpath):
		viewsPath = os.path.join(self.appDir, "views")
		tempPath = []
		for s in URLpath[:]:
			viewsPath = os.path.join(viewsPath, s)
			tempPath.append(URLpath.pop(0))
			if os.path.exists(viewsPath + '.xml'):
				break
			elif os.path.isdir(viewsPath):
				if not URLpath: # last loop
					if os.path.exists(os.path.join(viewsPath, 'default.xml')):
						tempPath.append('default')
					else:
						tempPath = ['notFound']
			else:
				tempPath, URLpath = ['notFound'], []
				break
		return (tempPath, URLpath)

	#lazy view objects creation
	def getView(self,acenv):
		path = acenv.URLpath or ['default']
		t = self.findCachedView(path[:]) # we have to work on a copy, because of next call with path in arguments
		if t:
			(v, acenv.viewPath, acenv.inputs) = t
		else:
			(acenv.viewPath, acenv.inputs) = self.findViewFile(path)
			if acenv.viewPath == ['notFound']:
				t = self.findCachedView(['notFound'])
				if t:
					return t[0]
			#print 'View not in cache'
			v = View(acenv.viewPath, self)
			self.cacheView(acenv.viewPath, v)
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
		view=self.getView(acenv)
		view.generate(acenv)
		#this is little faster than Object
		acenv.generations["lang"]=("object",{"name":"acf:lang","current":acenv.lang,"supported":",".join(acenv.langs)},None)
		acenv.generations["domain"]=("object",{"name":"acf:appDetails","domain":acenv.domain},None)
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
			defaultLang=attrs["default"].strip()
		except KeyError:
			#make it log.warning and fall back to en
			raise Exception("Misconfiguration of 'langs' setting in app configuration file.")
		#["","aaa"," dd   "]->["aaa","ddd"]
		self.langs=filter(len, map(str.strip, [defaultLang]+attrs.get("supported", "").split(",")))
		self.lang=self.langs[0]

	def __str__(self):
		return str(self.__dict__)

	def __setattr__(self, name, val):
		if self.immutable and not name=="DEFAULT_DB":
			if D: log.error("%s is read only",name)
			raise Exception("PropertyImmutable")
		self.__dict__[name]=val
