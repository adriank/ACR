# -*- coding: utf-8 -*-

# AsynCode Framework - XML framework allowing developing internet
# applications without using programming languages.
# Copyright (C) 2008-2010  Adrian Kalbarczyk, Sebastian Lis

# This program is free software: you can redistribute it and/or modify
# it under the terms of the version 3 of GNU General Public License as published by
# the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ACF.components import Component
from ACF.errors import *
from ACF.utils import replaceVars
from ACF.utils.generations import Object,List
from ACF.utils.xmlextras import tree2xml
import os
import shutil
import fnmatch

class FileSystem(Component):
	def __init__(self,config):
		#self.config=config
		#TODO check whether it is path to proper directory (exists, permissions etc) or not
		self.SHOW_DIRS=True
		self.SHOW_HIDDEN=False
		self.path=config[0][2][0]

	#TODO identify directories in an output!!!
	def list(self,acenv,conf):
		D=acenv.doDebug
		fullpath=conf["fullpath"]
		showDirs=conf.get("showdirs",self.SHOW_DIRS)
		showHidden=conf.get("showhidden",self.SHOW_HIDDEN)
		_filter=conf.get("filter",None)
		files=os.listdir(fullpath)
		if not showHidden:
			files=filter(lambda file: not file[0]==".",files)
		if not showDirs:
			files=filter(lambda file: not os.path.isdir(os.path.join(fullpath,file)),files)
		#WTF???
		#else:
			#if D: acenv.warning("'list' has bad value: showDirs=%s", showDirs)
		if _filter:
			files=filter(lambda file: fnmatch.fnmatch(file, _filter),files)
		#WTF???
		#if conf.get("extension","")=="hide":
		#	files=map(lambda f:	os.path.splitext(f)[0],files)
		files.sort()
		ret=[]
		if len(files)==0:
			o=Object()
			o.code="dirEmpty"
			return o
		path=conf["path"]
		for i in files:
			o=Object()
			o.name=i
			o.path=path
			ret.append(o)
		return List(ret)

	def create(self,acenv,conf,update=False):
		D=acenv.doDebug
		#path=os.path.join(self.path+conf["path"])
		#TODO if whole path do not exist -> create all dirs in path
		o=Object()
		if not update and os.path.isfile(conf["fullpath"]):
			o.status="error"
			o.code="fileExists"
			return o #return ("object",{"status":"error","code":"fileExists"},None)
		try:
			file=open(conf["fullpath"], 'w')
			#XXX this replace is pretty lame, need to investigate where the hell this \r is from, and do it cross-platform.
			file.write(conf["content"])#.replace("\r\n","\n"))
		except IOError,e:
			o.status="error"
			o.code="IOError"
			return cr #return ("object",{"status":"error","code":"IOError"},e)
		else:
			file.close()
		#o.status="ok"
		return o #return ("object",{"status":"ok"},None)

	def update(self,acenv,conf):
		return self.create(acenv,conf,True)

	def append(self,acenv,conf):
		D=acenv.doDebug
		o=Object()
		path=self.path+replaceVars(acenv,conf["path"])
		content=replaceVars(acenv,conf["content"])
		try:
			file=open(path, 'a')
			file.write(content.replace("\r\n","\n"))
		except IOError:
			#FIXIT
			print 'cannot open', path
		else:
			file.close()
		#o.status="ok"
		return ("object",{"status":"ok"},None)

	def delete(self,acenv,conf):
		D=acenv.doDebug
		o=Object()
		path=self.path+replaceVars(acenv,conf["path"])
		if (os.path.exists(path)):
			if (os.path.isfile(path)):
				os.remove(path)
			else:
				shutil.rmtree(path)
		#o.status="ok"
		return o

	def copy(self,acenv,conf):
		D=acenv.doDebug
		o=Object()
		copyFrom=self.path+replaceVars(acenv,conf["from"])
		copyTo=self.path+replaceVars(acenv,conf["to"])
		if (os.path.isfile(copyFrom)):
			shutil.copyfile(copyFrom, copyTo)
		return o

	def move(self,acenv,conf):
		o=Object()
		copyFrom=self.path+replaceVars(acenv,conf["from"])
		copyTo=self.path+replaceVars(acenv,conf["to"])
		if (os.path.isfile(copyFrom)):
			shutil.move(copyFrom, copyTo)
		return o

	def exists(self,acenv,conf):
		o=Object()
		path=self.path+replaceVars(acenv,conf["path"])
		o.exists=os.path.isfile(path)
		return o

	def get(self,acenv,conf):
		try:
			file=open(conf["path"],"r")
			content=file.read()
		except IOError,e:
			#FIXIT
			raise e
			#print 'cannot open', conf["path"]
		else:
			file.close()
		o=Object()
		o.content="<![CDATA["+content.replace("]]>","]]>]]&gt;<![CDATA[")+"]]>"
		return g

	def generate(self, acenv, config):
		D=acenv.doDebug
		if D:
			acenv.info("Component: 'FS'")
			acenv.info("Command: '%s'", replaceVars(acenv, config["command"]))
			# do poprawki
			if replaceVars(acenv,config["command"]) not in ("list", "create", "update", "append", "delete", "copy", "move", "exists", "get"):
				acenv.error("Command '%s' do not exist!", replaceVars(acenv, config["command"]))
		conf={}
		for i in config:
			if type(config[i]) is str:
				conf[i]=replaceVars(acenv, config[i])
			else:
				conf[i]=config[i]
			if D:
				if i!= "command": acenv.dbg("attribute: '%s', value: '%s'", i, conf[i])
		if D:
			if not conf["path"]:
				acenv.warning("path not suplied")
			elif conf["path"][0] !=  '/':
				acenv.warning("missning '/' character at the begginig of 'path' attribute")
		#if conf["path"][0]=="/":
		#	path=conf["path"][1:].split("/")
		#else: path=conf["path"].split()
		conf["fullpath"]=os.path.join(self.path,*conf["path"].split("/"))
		return self.__getattribute__(conf["command"])(acenv,conf)

	def parseAction(self, conf):
		ret={"command":conf["command"]}
		ret.update(conf["params"])
		if conf["content"]:
			s=[]
			for elem in conf["content"]:
				if type(elem) is tuple:
					s.append(tree2xml(elem))
				elif type(elem) is str:
					s.append(elem)
			ret["content"]="\n".join(s)
		return ret

def getObject(config):
	return FileSystem(config)
