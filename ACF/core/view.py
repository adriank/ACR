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
from ACF.utils import conditionchecker,getStorage
from ACF.utils.interpreter import execute,make_tree
from ACF.utils.checktype import checkType
import logging
import os

log=logging.getLogger('ACF.core.View')
D=logging.doLog
DEFINE="define"
SET="set"
OPERATION="command"

def parseInputs(nodes):
	if not nodes:
		return None
	ret=[]
	for i in nodes:
		attrs=i[1]
		ret.append({
			"name":attrs["name"],
			"type":attrs.get("type",None),
			"default":attrs.get("default",None)
		})
	return ret

class View(object):
	immutable=False
	timestamp=0 #file modification timestamp
	path="" #file path
	def __init__(self,name,app):
		if D: log.info("Created %s",name)
		#All "static" computations should be here. Don't do it inside handle!
		self.name=name
		self.app=app
		self.path=globals.appDir+"/views/"+name+".xml"
		try:
			self.timestamp=os.stat(self.path).st_mtime
			tree=xml2tree(self.path)
		except:
			self.immutable=True
			return
		#the order of inputs is meaningful - needs to be list
		#__dict__ is used because I don't know if it is good idea, easily changeable to self.config
		ns={}
		if not tree[1]:
			return
		for i in tree[1]:
			if i.startswith("xmlns:"):
				key=i.split(":")[1]
				value=tree[1][i].split("/").pop().lower()
				ns[key]=value
		self.namespaces=ns
		self.post=parseInputs(tree.get("/post/param")) or []
		inputs=[]
		self.conditions=[]
		actions=[]
		self.output=None
		for i in tree[2]:
			if i[0]=="param":
				inputs.append(i)
			elif i[0]=="condition":
				self.conditions.append(i)
			elif i[0]=="output":
				output=i
			else:
				actions.append(i)
		self.actions=self.parseActions(actions)
		#print self.actions
		self.inputs=parseInputs(inputs)
		if not self.actions:
			self.immutable=True
			return
		#don't check type of default value. Might be an error msg.
		#inputs={}
		#if D: log.debug("Setting defaults for inputs")
		#for i in self.inputs:
		#	if not i["default"]:
		#		self.needsParameters=True
		#	inputs[i["name"]]=i["default"]
		#self.inputDefaults=inputs
		if D: log.debug("Setting defaults for posts")
		posts={}
		for i in self.post:
			posts[i["name"]]=i["default"]
		self.postDefaults=posts
		#past here this object MUST be immutable
		self.immutable=True

	def parseActions(self,a):
		ret=[]
		try:
			for i in a:
				attrs=i[1]
				if D: log.debug("parsing action '%s' config for component %s",attrs.get("name","NotSet"),attrs["component"])
				action=NS2Tuple(i[0])[1]
				ns=None
				COMMAND="default"
				if i[1].has_key(COMMAND):
					ns,COMMAND=NS2Tuple(i[1][COMMAND])
				componentName=self.namespaces.get(ns,"default")
				ret.append({
					"type":action,#DEFINE or SET
					"COMMAND":COMMAND,#COMMAND name
					"name":attrs.get("name",None),
					"component":componentName,
					"condition":make_tree(attrs.get("condition",None)),
					"config":self.app.getComponent(componentName).parseAction(i)
				})
		except Error,e:
			pass
		return ret

	def __setattr__(self, name, val):
		if self.immutable:
			if D: log.error("%s is read only",name)
			raise Exception("PropertyImmutable")
		self.__dict__[name]=val

	def fillInputs(self,acenv):
		list=acenv.inputs
		if not self.inputs or not len(self.inputs):
			if D: log.debug("list of inputs empty. Returns 'True'.")
			return True
		if D: log.debug("All parameters were specified")
		i=-1 #i in for is not set if len returns 0
		inputsLen=len(self.inputs)
		for i in xrange(0,inputsLen):
			type=self.inputs[i]["type"]
			value=list[i]
			if not type or checkType(type,value):
				if type=="csv":
					value=value.split(",")
				acenv.requestStorage[self.inputs[i]["name"]]=value
			else:
				if D: log.error("Input value %s didn't pass the type check",acenv.requestStorage[i]["name"])
		for i in xrange(i+1,inputsLen):
			default=self.inputs[i]["default"]
			if default:
				acenv.requestStorage[self.inputs[i]["name"]]=default

	def checkConditions(self,acenv, conditions):
		if D: log.debug("Executed with acenv=%s and conditions=%s",acenv,conditions)
		try:
			for cond in conditions:
				r=conditionchecker.check(cond,data)
		except Error,e:
			if D: log.warning("Condition not fulfilled, %s",e)
			if cond["showError"]:
				raise Error(e)
			else:
				return False
		return True

	def generate(self,acenv):
		try:
			self.inputs
		except:# inputs is undefined
			acenv.generations.append(("object",{"type":"view","name":self.name},None))
			self.transform(acenv)
			return
		if D: log.debug("Executing with env=%s",acenv)
		self.fillInputs(acenv)
		for action in self.actions:
			if action["condition"] and not execute(acenv,action["condition"]):
				#TODO if SET is used in action -> log.error
				if action["type"]==SET:
					break
				continue
			component=self.app.getComponent(action["component"])
			#object or list
			nodes=component.generate(acenv,action["config"])
			if action["type"]==DEFINE:
				if D: log.info("Executing action=%s",action)
				if type(nodes) is tuple:
					nodes[1]["name"]=action["name"]
					nodes[1]["view"]=self.name
					acenv.generations.append(nodes)
				elif type(nodes) is list:
					acenv.generations.append(("list",{"name":action["name"],"view":self.name},nodes))
			elif action["type"]==SET:
				if D: log.info("Executing SET=%s",action)
				getStorage(acenv,action.get("storage","rs"))[action["name"]]=nodes[2]

	def transform(self,acenv):
		if not acenv.output["engine"]:
			acenv.tree=("list",{},[])
			for i in acenv.generations:
				acenv.tree[2].append(i)
