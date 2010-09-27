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
from ACF import globals
from ACF import components
from ACF.errors import *
from ACF.utils import getStorage
from ACF.utils.interpreter import execute,make_tree
from ACF.utils.checktype import checkType
from ACF.components import Object, List
import os

D=True
DEFINE="define"
SET="set"
COMMAND="command"
INHERITS="inherits"

def parseParams(nodes,dictionary=False):
	if not nodes:
		return None
	if dictionary:
		ret={}
	else:
		ret=[]
	for i in nodes:
		attrs=i[1]
		if dictionary:
			ret[attrs["name"]]={
				"type":attrs.get("type",None),
				"default":attrs.get("default",None)
			}
		else:
			ret.append({
				"name":attrs["name"],
				"type":attrs.get("type",None),
				"default":attrs.get("default",None)
			})
	return ret

class View(object):
	#timestamp=0 #file modification timestamp
	#path="" file path
	def __init__(self, name, app, acenv):
		#if D: log.info("Created %s",name)
		#All "static" computations should be here. Don't do it inside handle!
		self.immutable=False
		self.name="/".join(name)
		self.app=app
		self.path=os.path.join(app.viewsPath,*name)+".xml"
		try:
			self.timestamp=os.stat(self.path).st_mtime
			tree=xml2tree(self.path)
		#TODO support more exception classes;
		except Exception,e:
			self.immutable=True
			raise e
			raise ViewNotFound("view '%s' not found"%(name))
		#the order of inputs is meaningful - needs to be list
		ns={}
		if not tree[1]:
			return
		#parses xmlns: attributes and extracts namespaces
		for i in tree[1]:
			if i.startswith("xmlns:"):
				key=i.split(":")[1]
				value=tree[1][i].split("/").pop().lower()
				ns[key]=value
		self.namespaces=ns
		inputs=[]
		self.conditions=[]
		actions=[]
		posts=[]
		output=[]
		try:
			acenv.URLpath = filter(lambda x: not str.isspace(x) and len(x)!=0,tree[1]["inherits"]  .split("/"))
			self.parent = app.getView(acenv)
			#if D: acenv.debug("Loaded base view: %s" % tree[1]["inherits"])
		except:
			self.parent = None
			#if D: acenv.debug("Loading a root view.")
		for i in tree[2]:
			if i[0]=="param":
				inputs.append(i)
			elif i[0]=="condition":
				self.conditions.append(i)
			elif i[0]=="output":
				output.append(i)
			elif i[0]=="post":
				posts=i[2]
			elif i[0] in [SET,DEFINE]:
				actions.append(i)
		if self.parent:
			self.rawActions = self.parent.rawActions + actions
		else:
			self.rawActions = actions
		self.actions = self.parseActions(self.rawActions)
		self.inputs=parseParams(inputs)
		self.posts=parseParams(posts,True)
		self.output={}
		try:
			self.output["format"]=output[0][1]["format"]
		except:
			pass
		try:
			self.output["xsltfile"]=output[0][1]["xsltfile"]
		except:
			pass
		try:
			self.outputConfig=output[0][1]["config"]
		except:
			outputConfig="config"
		if not self.actions:
			self.immutable=True
			return
		#if D: log.debug("Setting defaults for posts")
		#past here this object MUST be immutable
		self.immutable=True

	def parseActions(self,a):
		ret=[]
		try:
			for i in a:
				attrs=i[1]
				#if D: log.debug("parsing action '%s' config for component %s",attrs.get("name","NotSet"),attrs["component"])
				action=NS2Tuple(i[0])[1]
				ns=None
				cmd="default"
				if i[1].has_key(COMMAND):
					ns,cmd=NS2Tuple(i[1][COMMAND])
				componentName=self.namespaces.get(ns,"default")
				params={}
				if ns:
					for j in i[1]:
						if j.startswith(ns+":") and not j==ns+cmd:
							params[j.split(":").pop()]=i[1][j]
				actionConfig={
					"command":cmd,
					"params":params,
					"content":i[2]
				}
				before = attrs.get("before", None)
				after = attrs.get("after", None)
				o = {
					"type":action,#DEFINE or SET
					"command":cmd,#command name
					"name":attrs.get("name",None),
					"component":componentName,
					"condition":make_tree(attrs.get("condition",None)),
					"config":self.app.getComponent(componentName).parseAction(actionConfig),
				}
				if before:
					n,name=0,before
					if before=='*':
						ret.insert(0, o)
						continue
				elif after:
					n,name=1,after
					if after=='*':
						ret.append(o)
						continue
				i=0
				try:
					while not ret[i]["name"] == name:
						i+=1
				except:
					ret.append(o)
				else:
					ret.insert(i+n, o)

				#try:
				#	ret.insert(self.searchAction(ret, before, after), o)
				#except:
				#	ret.append(act)
		except Error,e:
			pass
		return ret

	def __setattr__(self, name, val):
		if name!="immutable" and self.immutable:
			#if D: log.error("%s is read only",name)
			raise Exception("PropertyImmutable")
		self.__dict__[name]=val

	def fillPosts(self,acenv):
		#TODO add default values support by doing ticket #13
		#if D: acenv.info("Create '%s' view",(self.name))
		list=acenv.posts
		if not self.posts or not len(self.posts):
			#if D: log.debug("list of posts is empty. Returning 'True'.")
			return True
		#TODO debug the key names. Forms should have keys specified in <post/> parameters!
		for i in list:
			value=list[i]
			type=self.posts[i]["type"]
			if not type or checkType(type,value):
				if type=="csv":
					value=value.split(",")
				acenv.requestStorage[i]=value

	def fillInputs(self,acenv):
		list=acenv.inputs
		if not self.inputs or not len(self.inputs):
			#if D: log.debug("list of inputs is empty. Returning 'True'.")
			return True
		#if D: log.debug("All parameters were specified")
		i=-1 #i in for is not set if len returns 0
		if list:
			inputsLen=min([len(self.inputs),len(list)])
		else:
			inputsLen=0
		for i in xrange(0,inputsLen):
			type=self.inputs[i]["type"]
			value=list[i]
			if not type or checkType(type,value):
				if type=="csv":
					value=value.split(",")
				acenv.requestStorage[self.inputs[i]["name"]]=value
			#else:
			#	if D: log.error("Input value %s didn't pass the type check",acenv.requestStorage[i]["name"])
		for i in xrange(i+1,len(self.inputs)):
			default=self.inputs[i]["default"]
			if default:
				acenv.requestStorage[self.inputs[i]["name"]]=default

	def generate(self,acenv):
		D=acenv.doDebug
		try:
			self.inputs
		except:# inputs is undefined
			acenv.generations.append(("object",{"type":"view","name":self.name},None))
			self.transform(acenv)
			return
		#if D: log.debug("Executing with env=%s",acenv)
		self.fillInputs(acenv)
		self.fillPosts(acenv)
		acenv.requestStorage["__lang__"]=acenv.lang
		for action in self.actions:
			if D: acenv.info("define name='%s'",action["name"])
			if action["condition"] and not execute(acenv,action["condition"]):
				#TODO if SET is used in action -> log.error
				if action["type"]==SET:
					break
				continue
			component=self.app.getComponent(action["component"])
			#object or list
			generation=component.generate(acenv,action["config"])
			if not generation:
				raise Error("ComponentError","Component did not return proper value. Please contact component author.")
			if not action["name"]:
					continue
			if action["type"]==DEFINE:
				#if D: log.info("Executing action=%s",action)
				generation.name=action["name"]
				generation.view=self.name
				acenv.generations[action["name"]]=generation
			elif action["type"]==SET:
				#if D: log.info("Executing SET=%s",action)
				ns,name=NS2Tuple(action["name"],"::")
				getStorage(acenv,ns or "rs")[name]=generation
		try:
			acenv.output["format"]=self.output["format"]
		except:
			pass
		try:
			acenv.output["xsltfile"]=self.output["xsltfile"]
		except:
			pass
		#print "generations"
		#print acenv.generations

	def isUpToDate(self):
		return self.timestamp >= os.stat(self.path).st_mtime
