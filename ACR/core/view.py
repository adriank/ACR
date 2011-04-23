#!/usr/bin/env python
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

from ACR.utils.xmlextras import *
from ACR import acconfig
from ACR import components
from ACR.errors import *
from ACR.utils import getStorage,prepareVars,typesMap,str2obj
from ACR.utils.interpreter import make_tree
import os,re

NODE="node"
SET="set"
PUSH="push"
INSERT="insert"
WRITE_COMMANDS=[SET,PUSH,INSERT]
ACTIONS=WRITE_COMMANDS+[NODE]
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
		typ=typesMap.get(attrs.get("type","default").lower())()
		if attrs.has_key("default"):
			typ.setDefault(make_tree(attrs["default"]))
		else:
			postCount+=1
		ret[attrs["name"]]=typ
	return (ret,postCount)

def parseInputs(nodes):
	if not nodes:
		return None
	ret=[]
	postCount=0
	for i in nodes:
		attrs=i[1]
		try:
			typ=typesMap.get(attrs.get("type","default").lower())()
		except TypeError:
			raise Error("WrongInputTypeName","Input type '%s' is not supported."%attrs.get("type","default"))
		if attrs.has_key("default"):
			typ.setDefault(make_tree(attrs["default"]))
		ret.append({
			"name":attrs["name"],
			"type":typ
		})
	return ret

class View(object):
	def __init__(self, name, app):
		#All "static" computations should be here. Don't do it inside handle!
		#setting immutable because of setter
		self.immutable=False
		self.name=".".join(name)
		self.app=app
		self.path=os.path.join(app.viewsPath,*name)+".xml"
		#try:
		self.timestamp=os.stat(self.path).st_mtime
		tree=xml2tree(self.path, True)
		#TODO support more exception classes;
		#except Exception,e:
		#	self.immutable=True
		#	raise ViewNotFound("view '%s' not found"%(name))
		ns={}
		attrs=tree[1]
		if not attrs:
			return
		#parses "xmlns:" attributes and extracts namespaces
		for i in attrs:
			if i.startswith("xmlns:"):
				key=i.split(":",1)[1]
				value=attrs[i].rsplit("/",1)[1].lower()
				ns[key]=value
		self.namespaces=ns
		#checks whether view inherits from another view
		try:
			self.parent=app.getView(filter(lambda x: len(x) and not str.isspace(x), attrs["inherits"].split("/")),True)[0]
		except KeyError:
			self.parent=None
		except (IOError):
			raise Error("ParentViewNotFound","View '%s' not found."%attrs["inherits"])
		except Exception,e:
			raise Error("ParentViewError",str(e))
		inputSchemas=[]
		conditions=[]
		actions=[]
		postSchemas=[]
		output=[]

		for node in tree[2]:
			if type(node) is str:
				continue
			name=node[0]
			if name=="param":
				inputSchemas.append(node)
			elif name=="condition":
				conditions.append(node)
			elif name=="output":
				output.append(node)
			elif name=="post":
				postSchemas=filter(lambda x: type(x) is not str, node[2])
			elif name in ACTIONS:
				actions.append(node)
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
			self.output["xsltfile"]=str2obj(output[0][1]["xsltfile"])
		except: pass
		try:
			self.output["xslt-force-reload"]=str2obj(output[0][1]["xslt-force-reload"])
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
		#past here this object MUST be immutable
		self.immutable=True

	def parseConditions(self, a):
		ret=[]
		for i in a:
			attrs=i[1]
			if not attrs:
				attrs={"name":"unnamedCondition"}
			ret.append({
				"name":attrs.get("name"),
				"value":make_tree(attrs.get("value") or "".join(i[2]).strip())
			})
		return ret

	def checkConditions(self, acenv):
		for i in self.conditions:
			if i["value"] and not i["value"].execute(acenv):
				raise Error("ConditionNotSatisfied", "Condition %s is not satisfied."%i["name"])
		return True

	#def importAction(self,action):
	#	path=re.split("/*",action[1].get("path"))
	#	v=self.app.getView(path[:-1])[0]
	#	for a in v.actions:
	#		if a["name"]==path[-1]:
	#			ret.append(a)
	#			ret[-1]["name"]=action[1].get("name", None)
	#			break

	def parseAction(self,action):
		""" Gets tuple representation of action XML element and returns dict-based configuration """
		attrs=action[1]
		ns,cmd=NS2Tuple(attrs.get(COMMAND,"default"))
		params={}
		if ns:
			for attr in attrs:
				if attr.startswith(ns+":") and not attr==ns+cmd:
					params[attr.rsplit(":",1)[1]]=prepareVars(action[1][attr])
		ret={
			"command":cmd,
			"params":params,
			"content":action[2]
		}
		if action[0]==NODE:
			ret["output"]=True
		return ret

	def parseActions(self,actions):
		def findAction(actions,name):
			if not name:
				return None
			i=len(actions)-1
			if i<0:
				return None
			try:
				while not actions[i]["name"]==name:
					i-=1
				return i
			except:
				return None
			else:
				return len(actions)

		ret=self.parent and self.parent.actions[:] or []
		for action in actions:
			#if i[0]=="import":
			#	self.importAction(i[0])
			#	continue
			typ=action[0]
			attrs=action[1]
			ns,cmd=NS2Tuple(attrs.get(COMMAND,"default"))
			componentName=self.namespaces.get(ns,"default")
			o={
				"type":typ,#NODE or SET
				#"command":cmd,#command name
				"name":attrs.get("name",None),
				"component":componentName,
				"config":self.app.getComponent(componentName).parseAction(self.parseAction(action)),
			}
			if attrs.has_key("default"):
				o["default"]=make_tree(attrs["default"])
			if attrs.has_key("path"):
				o["path"]=make_tree(attrs["path"])
			if attrs.has_key("condition"):
				o["condition"]=make_tree(attrs["condition"])
			# positions the action in the list of actions
			before=attrs.get("before")
			after=attrs.get("after")
			#TODO this is nowhere near clearness. Need to write reference on inheritance regarding before/after and then implement it here
			posInParent=None
			if o["type"]==NODE:
				if not o["name"]:
					raise Error("noNodeNameError", "Nodes must have names set.")
				pos=findAction(ret,o["name"])
				if pos>-1 and ret[pos]["type"]==NODE:
					#print "WARNING: node %s overwritten"%(o["name"])
					ret.pop(pos)
			if before:
				if before=='*':
					ret.insert(0, o)
				else:
					try:
						ret.insert(findAction(ret,before),o)
					except:
						ret.append(o)
			elif after:
				if after=='*':
					ret.append(o)
				else:
					try:
						ret.insert(findAction(ret,after)+1,o)
					except:
						ret.append(o)
			else:
				ret.append(o)
		#for i in ret:
		#	print i["name"]
		return ret

	def fillPosts(self,acenv):
		D=acenv.doDebug
		if D:
			acenv.debug("START View:fillPosts")
		if not self.postSchemas or not len(self.postSchemas):
			if D:
				acenv.debug("posts schema is empty.")
				acenv.debug("END View:fillPosts with: 'True'.")
			return True
		if D:
			acenv.debug("postSchemas is %s",self.postSchemas)
			acenv.debug("posts is %s",acenv.posts)
		list=acenv.posts
		if not list or len(list)<self.postCount:
			raise Error("notEnoughPostFields","Not enough post fields, is %s and must be %s"%(len(list),self.postCount))
		postSchemas=self.postSchemas
		try:
			for i in postSchemas:
				value=list.get(i)
				typ=postSchemas[i]
				acenv.requestStorage[i]=typ.get(acenv,value)
		except Error, e:
			if e.name=="NotValidValue":
				raise Error("NotValidValue", "Value of %s is invalid, %s"%(i,e))
			else:
				raise e
		if D:acenv.debug("requestStorage is %s",acenv.requestStorage)
		if D:acenv.debug("END View:fillPosts")

	def fillInputs(self,acenv):
		D=acenv.doDebug
		if D: acenv.debug("START fillInputs")
		inputSchemas=self.inputSchemas
		if D: acenv.debug("inputSchemas are: %s",inputSchemas)
		if not inputSchemas or not len(inputSchemas):
			if D: acenv.debug("END View:fillInputs with: list of inputs is empty")
			return True
		list=acenv.inputs
		if D: acenv.debug("inputs are: %s",list)
		for i in inputSchemas:
			typ=i["type"]
			#TODO change to:
			#acenv.requestStorage[i["name"]]=typ.get(acenv,list.pop(0))
			try:
				typ.set(list.pop(0))
			except:
				pass
			try:
				acenv.requestStorage[i["name"]]=typ.get(acenv)
			except Error, e:
				if e.name=="NotValidValue":
					raise Error("NotValidValue", "Value of '%s' is invalid."%(i["name"]))
				else:
					raise e
		if D:
			acenv.debug("RS is: %s",acenv.requestStorage)
			acenv.debug("END View:fillInputs")

	def generate(self,acenv):
		D=acenv.doDebug
		if D: acenv.debug("START View.generate of view: %s",self.name)
		try:
			self.inputSchemas
		except:# inputs is unNODEd
			acenv.generations.append({"type":"view","name":self.name})
			self.transform(acenv)
			return
		#if D: acenv.debug("Executing with env=%s",acenv)
		self.fillInputs(acenv)
		self.fillPosts(acenv)
		acenv.requestStorage["__lang__"]=acenv.lang
		self.checkConditions(acenv)
		for action in self.actions:
			if D: acenv.info("\033[92mdefining name='%s'\033[0m",action["name"])
			action_type=action["type"]
			path_set=action.has_key("path")
			if action.has_key("condition") and not action["condition"].execute(acenv):
				if D: acenv.warning("Condition is not meet")
				if action_type in WRITE_COMMANDS:
					default=action.get("default")
					if default:
						if path_set:
							if action_type==PUSH:
								pointer=action["path"].execute(acenv)
								if type(pointer) is not list:
									raise Error("NotArrayError", "Path did not return array.")
								pointer.append(default.execute(acenv))
								continue
						getStorage(acenv,"rs")[action["name"]]=default.execute(acenv)
				continue
			component=self.app.getComponent(action["component"])
			generation=component.generate(acenv,action["config"])
			if action_type==NODE and type(generation) is dict and not generation.has_key("@status"):
				generation["@status"]="ok"
			#if not generation:
			#	raise Error("ComponentError","Component did not return proper value. Please contact component author.")
			#if not action["name"]:
			#		continue
			if path_set:
				if action_type==PUSH:
					pointer=action["path"].execute(acenv)
					if action_type==PUSH and type(pointer) is not list:
						raise Error("NotArrayError", "Path did not return array.")
					if D: acenv.info("Appending %s to %s",generation,action["path"])
					pointer.append(generation)
					print pointer
					#elif action["type"]==SET:
				#	pointer=generation
			else:
				if action["type"]==NODE:
					if D: acenv.info("Adding node %s with: %s",action["name"],generation)
					#generation.name=action["name"]
					#generation.view=self.name
					acenv.generations[action["name"]]=generation
				elif action["type"]==SET:
					if D: acenv.info("Setting %s with: %s",action["name"],generation)
					getStorage(acenv,"rs")[action["name"]]=generation
		if acenv.output:
			acenv.output.update(self.output)

	def isUpToDate(self):
		"""
			Parent is not up to date and
			self is not refreshed after parent change and
			file is changed
			-> false
		"""
		if self.parent:
			if not self.parent.isUpToDate():
				return False
			#TODO needs new attribute storing parsing time
			if self.timestamp < self.parent.timestamp:
			#	print "parent timestamp",self.timestamp," ",self.parent.timestamp
				return False
		if self.timestamp < os.stat(self.path).st_mtime:
			return False
		return True

	def __setattr__(self, name, val):
		if name!="immutable" and self.immutable:
			#if D: log.error("%s is read only",name)
			raise Exception("PropertyImmutable")
		self.__dict__[name]=val

	def __str__(self):
		return "View(%s)"%self.name
