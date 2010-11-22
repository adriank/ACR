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
IMPORT="import"

def parsePosts(nodes):
	if not nodes:
		return (None,None)
	ret={}
	postCount=0
	for i in nodes:
		attrs=i[1]
		default=attrs.get("default",None)
		ret[attrs["name"]]={
			"type":attrs.get("type",None),
			"default":default
		}
		if default:
			postCount+=1
	return (ret,postCount)

def parseInputs(nodes):
	if not nodes:
		return None
	ret=[]
	postCount=0
	for i in nodes:
		attrs=i[1]
		ret.append({
			"name":attrs["name"],
			"type":attrs.get("type",None),
			"default":attrs.get("default",None)
		})
	return ret

class View(object):
	#timestamp=0 #file modification timestamp
	#path="" file path
	def __init__(self, name, app):
		#if D: log.info("Created %s",name)
		#All "static" computations should be here. Don't do it inside handle!
		#setting immutable because of setter
		self.immutable=False
		self.name="/".join(name)
		self.app=app
		self.path=os.path.join(app.viewsPath,*name)+".xml"
		#try:
		self.timestamp=os.stat(self.path).st_mtime
		tree=xml2tree(self.path, True)
		#TODO support more exception classes;
		#except Exception,e:
		#	self.immutable=True
		#	raise e
		#	raise ViewNotFound("view '%s' not found"%(name))
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
		inputSchemas=[]
		conditions=[]
		actions=[]
		postSchemas=[]
		output=[]
		try:
			self.parent = app.getView(filter(lambda x: not str.isspace(x) and len(x)!=0,tree[1]["inherits"]  .split("/")))[0]
			#if D: acenv.debug("Loaded base view: %s" % tree[1]["inherits"])
		except:
			self.parent = None
		for i in tree[2]:
			if type(i) is str:
				continue
			elif i[0]=="param":
				inputSchemas.append(i)
			elif i[0]=="condition":
				conditions.append(i)
			elif i[0]=="output":
				output.append(i)
			elif i[0]=="post":
				postSchemas=filter(lambda x: type(x) is not str, i[2])
			elif i[0] in [SET,DEFINE,IMPORT]:
				actions.append(i)
		self.conditions=self.parseConditions(conditions)
		self.actions=self.parseActions(actions)
		self.inputSchemas=parseInputs(inputSchemas) or []
		if self.parent and self.parent.inputSchemas:
			self.inputSchemas=self.parent.inputSchemas+self.inputSchemas
		self.postSchemas, self.postCount=parsePosts(postSchemas)
		self.output={}
		try:
			self.output["format"]=output[0][1]["format"]
		except: pass
		try:
			self.output["xsltfile"]=output[0][1]["xsltfile"]
		except: pass
		try:
			self.outputConfig=output[0][1]["config"]
		except:
			outputConfig="config"
		# TODO check if it is correct
		## output inheritance
		#if self.parent and self.parent.outputFormat:
		#		self.outputFormat=self.parent.outputFormat
		#		self.outputConfig=self.parent.outputConfig
		## posts inheritance
		#if self.parent and self.parent.posts:
		#	self.posts=self.parent.posts
		#if not self.actions:
		#	self.immutable=True
		#	return
		#if D: log.debug("Setting defaults for posts")
		#past here this object MUST be immutable
		self.immutable=True

	def parseConditions(self, a):
		ret=[]
		for i in a:
			attrs=i[1]
			ret.append({
				"name": attrs.get("name", None),
				"value": make_tree(attrs.get("value", None) or "".join(i[2]).strip())
			})
		return ret

	def checkConditions(self, acenv):
		for i in self.conditions:
			if i["value"] and not execute(acenv, i["value"]):
				return False
		return True

	def parseActions(self,a):
		if self.parent:
			ret=self.parent.actions[:]
		else:
			ret = []
		#try:
		for i in a:
			# import should check befere and after?
			if i[0]=="import":
				path=filter(lambda x: not str.isspace(x) and len(x)!=0,i[1].get("path", None).split("/"))
				v=self.app.getView(path[:-1])[0]
				for a in v.actions:
					if a["name"]==path[-1]:
						ret.append(a)
						ret[-1]["name"] = i[1].get("name", None)
						break
				continue
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
				"default":i[1].get("default",None),
				"config":self.app.getComponent(componentName).parseAction(actionConfig),
			}
			#WTF??? n, name??
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
				# TODO raise Error('View not found')
				ret.append(o)
				#raise Error('View not found')
			else:
				ret.insert(i+n, o)
		#except Error,e:
			#pass
		return ret

	def __setattr__(self, name, val):
		if name!="immutable" and self.immutable:
			#if D: log.error("%s is read only",name)
			raise Exception("PropertyImmutable")
		self.__dict__[name]=val

	def fillPosts(self,acenv):
		#TODO add default values support by doing ticket #13
		if D: acenv.info("Create '%s' view",(self.name))
		if not self.postSchemas or not len(self.postSchemas):
			if D: acenv.debug("list of posts is empty. Returning 'True'.")
			return True
		list=acenv.posts
		if not list or len(list)<self.postCount:
			#TODO normalize the Error messages!
			raise Error("Not enough post fields")
		#TODO debug the key names. Forms should have keys specified in <post/> parameters!
		for i in self.postSchemas:
			value=list.get(i,self.postSchemas[i]["default"])
			type=self.postSchemas[i]["type"]
			if not type or checkType(type,value):
				if type=="csv":
					value=value.split(",")
				acenv.requestStorage[i]=value
			else:
				raise Error("Wrong data type suplied")

	def fillInputs(self,acenv):
		list=acenv.inputs
		if not self.inputSchemas or not len(self.inputSchemas):
			if D: acenv.debug("list of inputs is empty. Returning 'True'.")
			return True
		#XXX this comment is not true
		#if D: acenv.debug("All parameters were specified")
		i=-1 #i in for is not set if len returns 0
		if list:
			inputsLen=min([len(self.inputSchemas),len(list)])
		else:
			inputsLen=0
		for i in xrange(0,inputsLen):
			type=self.inputSchemas[i]["type"]
			value=list[i]
			if not type or checkType(type,value):
				if type=="csv":
					value=value.split(",")
				acenv.requestStorage[self.inputSchemas[i]["name"]]=value
			#else:
			#	if D: log.error("Input value %s didn't pass the type check",acenv.requestStorage[i]["name"])
		for i in xrange(i+1,len(self.inputSchemas)):
			default=self.inputSchemas[i]["default"]
			#Keep is not None; "" is valid value!
			if default is not None:
				acenv.requestStorage[self.inputSchemas[i]["name"]]=default

	def generate(self,acenv):
		D=acenv.doDebug
		try:
			self.inputSchemas
		except:# inputs is undefined
			acenv.generations.append(("object",{"type":"view","name":self.name},None))
			self.transform(acenv)
			return
		#if D: acenv.debug("Executing with env=%s",acenv)
		self.fillInputs(acenv)
		self.fillPosts(acenv)
		acenv.requestStorage["__lang__"]=acenv.lang
		for action in self.actions:
			if D: acenv.info("define name='%s'",action["name"])
			if action["condition"] and not execute(acenv,action["condition"]):
				if D: acenv.warning("Condition is not meet")
				if action["type"]==SET:
					if D: acenv.warning("Set condition is not meet.")
					ns,name=NS2Tuple(action["name"],"::")
					getStorage(acenv,ns or "rs")[name]=action.get("default") or ""
				continue
			component=self.app.getComponent(action["component"])
			#object or list
			generation=component.generate(acenv,action["config"])
			if not generation:
				raise Error("ComponentError","Component did not return proper value. Please contact component author.")
			if not action["name"]:
					continue
			if action["type"]==DEFINE:
				if D: acenv.info("Executing action=%s",action)
				generation.name=action["name"]
				generation.view=self.name
				acenv.generations[action["name"]]=generation
			elif action["type"]==SET:
				if D: acenv.info("Executing SET=%s",action)
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

	def isUpToDate(self):
		return self.timestamp >= os.stat(self.path).st_mtime
