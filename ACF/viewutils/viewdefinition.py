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

from itertools import izip
from ACF import globals
from ACF.utils.checktype import checkType
from ACF.viewutils import configprovider as CP
#from ACF.utils.conditionchecker import check
from ACF.errors import *
from ACF.session.file import FileSession
from ACF.utils.xmlextras import tree2xml
from ACF.utils import fakeaccount
import re
try:
	import simplejson
except:
	pass
import logging

log = logging.getLogger('ACF.View')

class View:
	inputs=[]
	configs=[]
	requestData={}
	post=[]
	def __init__(self, name):
		log.info("Created %s",name)
		globals.requestStorage=self.requestData
		self.name=name
		try:
			t=CP.parseView(name)
		except CP.ViewError,e:
			log.error("ViewError")
			# TODO delete this
			self.error="ViewError"
			# TODO change to empty View (w/o config file)
			try:
				t=CP.parseView("notFound")
			except CP.ViewError:
				if globals.config.has_key("debug") and globals.config["debug"]:
					raise Error("ErrorViewNotFound")
				else:
					raise Error("ApplicationError")
		self.inputs=t["inputs"]
		self.post=t["post"]
		self.configs=t["configs"]
		self.conditions=t["conditions"]
		if t["output"] is not None:
			globals.request.output=t["output"]
		"""
		self.data is:
		{"name":"val"}
		"""
#		self.requestData={}
		for i in self.inputs:
			self.requestData[i["name"]]=i["default"]
		self.tree=("document",None,[])

	def fillInputs(self, list):
		log.debug("Executing with list=%s",(list))
		#no parameters needed
		if len(self.inputs) is 0:
			log.debug("list of inputs empty. Returns 'True'.")
			return True
		if list is None:
			log.debug("none of parameters were specified - data from default")
			list=[]
			for i in len(self.inputs):
				if i.has_key("default"):
					list.append(i["default"])
			if len(l)<len(self.inputs):
				log.error("ToFewGETParameters,Wrong number of parameters. Should be at least "+str(len(self.inputs))+" but is "+str(len(l)))
				raise Error("ToFewGETParameters","Wrong number of parameters. Should be at least "+str(len(self.inputs))+" but is "+str(len(l)))
			else:
				return True
		log.debug("All parameters were specified")
		for input, elem in izip(self.inputs,list):
			log.debug("input data type check")
			if input["type"] is not None and input["type"].lower()=="regexp":
				log.debug("%s is of regexp %s"(input["name"],input["re"]))
				import re
				if not re.match(input["re"],elem):
					input["type"]+=": "+input["re"]
					log.error("InputTypeError. Should be %s but is '%s'",(input["type"],elem))
					raise Error("InputTypeError","Should be "+input["type"]+" but is \""+elem+"\"")
			elif not checkType(input["type"],elem):
				log.error("InputTypeError. Should be %s but is '%s'",(input["type"],elem))
				raise Error("InputTypeError","Should be "+input["type"]+" but is \""+elem+"\"")
			self.requestData[input["name"]]=elem
		return True

	def fillPost(self,dict):
#		if len(self.post) > len(dict) > 0:
#			raise Error("WrongNumberOfParameters","Wrong number of parameters. Should be exactly "+str(len(self.post))+" but is "+str(len(dict)))
		for elem in self.post:
			if not dict.has_key(elem["name"]) and not elem.has_key("default"):
				log.error("%s was not suplied",elem["name"])
				raise Error("FieldNotFilledInError","POST do not have "+elem["name"]+" field filed in")
			if not dict.has_key(elem["name"]) and elem.has_key("default"):
				dict[elem["name"]]=elem["default"]
			if elem["type"]:
				try:
					if elem["type"]=="regexp":
						import re
						if not re.match(elem["re"],dict[elem["name"]]):
							log.error("%s did not match with %s",elem["name"],elem["re"])
							raise Error("InputTypeError","Should be "+elem["type"]+" and is \""+dict[elem["name"]]+"\"")
					elif not checkType(elem["type"],dict[elem["name"]]):
						raise Error("InputTypeError","Should be "+elem["type"]+" and is \""+dict[elem["name"]]+"\"")
				except Error,e:
					if not elem.has_key("default"):
						raise e
					else:
						dict[elem["name"]]=elem["default"]
			add=dict[elem["name"]]
			if 	elem["type"]=="csv":
				add=add.split(",")
				for i in add:
					i=i.strip()
			self.requestData[elem["name"]]=add
		return True

	def handle(self,o):
		log.debug("Executing with o=%s",(o))
		sessID=None
		tree=self.tree
		prefix=globals.prefix+"SESS"
		if globals.request.cookies.has_key(prefix):
			log.info("Session cookie found")
			sessID=globals.request.cookies[prefix]
			try:
				globals.session=FileSession(sessID)
			except:
				sessID=None
		if not sessID and globals.config["session"]["fakeAccount"]:
			log.info("There is no session cookie and fakeAccount is 'on'.")
			fakeaccount.create()
		if globals.session:
			log.debug("sessID is %s and session is %s",sessID,globals.session.data)
		#global conditions
		try:
			self.fillInputs(o["data"])
			if o["post"]:
				self.fillPost(o["post"])
			self.requestData["__lang__"]=globals.lang
			log.info("Checking global View conditions")
			for i in self.conditions:
				if check(i,self.requestData) is not True:
					log.error("%s, %s",i["errorCode"],i["errorString"])
					raise Error(i["errorCode"],i["errorString"])
		except Error, e:
			log.error("%s",e.get())
			tree[2].append(e.get())
			# conditions not fulfilled so we terminate all View
			return tree2xml(tree)

		childs=[]
		log.info("Executing actions")
		for i in self.configs:
			log.info("Starting %s action.",i["name"])
			name="ACF.components."+i["component"]
			__import__(name)
			import sys
			module=sys.modules[name]
			component=module.getObject(i["config"])
			log.debug("Component %s created",i["component"])
			ret=None
			try:
				#implement terminating option
				r=component.checkConditions(self.requestData)
				log.debug("checkConditions returned %s",r)
				ret=component.handle(self.requestData)
				log.debug("Action %s executed with result=%s",i["name"],ret)
				if i["name"] is not None:
					childs.append((i["name"],None,ret))
			except Error, e:
				raise e
				if i["name"]:
					log.error("%s",e.get())
					if globals.config.has_key("debug") and globals.config["debug"]:
						childs.append((i["name"],None,[e.get()]))
					else:
						tree[2].append("ApplicationError, Enter the debug mode to see details.")
			except TerminatingError, e:
				log.error("%s",e.get())
				if i["name"]:
					if globals.config.has_key("debug") and globals.config["debug"]:
						tree[2].append(e.get())
					else:
						tree[2].append("ApplicationError, Enter the debug mode to see details.")
				break
		tree[2].extend(childs)
		attrs={}
		log.info("sessID is %s",sessID)
		if sessID is not None:
			log.info("Generating &lt;user/>")
			if globals.session.has_key('loggedIn') and globals.session['loggedIn']:
				attrs={"email":globals.session['email'],"id":globals.session['ID']}
			elif globals.session.has_key("fake") and globals.session['fake']:
				attrs={"type":"fake","id":globals.session['ID']}
			if globals.session.has_key('role'):
				attrs["role"]=globals.session['role']
			log.debug("Creating 'user' node with attributes %s",attrs)
			tree[2].append(("user",attrs,None))
		if globals.session:
			globals.session.save()
		langs=[]
		if globals.langs:
			for i in globals.langs:
				langs.append((i,None,None))
		tree[2].append(("langs",{"current":globals.lang},langs))
		tree[2].append(("view",{"name":self.name},None))

	def getXML(self):
		log.info("Generating XML")
		return """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="/xslt/"""+globals.xsltFile+"\"?>\n"+tree2xml(self.tree).decode("utf-8")

	def getJSON(self):
		log.info("Generating JSON")
		try:
			return simplejson.dumps(self.tree)
		except:
			raise Exception("simplejson module not installed. Can't output JSON.")
