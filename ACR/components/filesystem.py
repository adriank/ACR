# -*- coding: utf-8 -*-

# Asyncode Runtime - XML framework allowing developing internet
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

from ACR.components import Component
from ACR.errors import *
from ACR.utils import prepareVars, replaceVars
from ACR.utils.generations import Object,List
from ACR.utils.xmlextras import tree2xml
import os
import shutil
import fnmatch

class FileSystem(Component):
	SHOW_DIRS=True
	SHOW_HIDDEN=False
	ONLY_DIRS=False
	def __init__(self,config):
		#self.config=config
		#TODO check whether it is path to proper directory (exists, permissions etc) or not
		self.abspath=config[0][2][0]

	def list(self,acenv,conf):
		D=acenv.doDebug
		fullpath=conf["fullpath"]
		showDirs=conf.get("showdirs",self.SHOW_DIRS)
		showHidden=conf.get("showhidden",self.SHOW_HIDDEN)
		onlyDirs=conf.get("onlydirs",self.ONLY_DIRS)
		_filter=conf.get("filter")
		all=os.listdir(fullpath)
		all.sort()
		if _filter:
			all=filter(lambda file: fnmatch.fnmatch(file, _filter),all)
		if not showHidden:
			all=filter(lambda file: not file[0]==".",all)
		if not onlyDirs:
			files=filter(lambda file: not os.path.isdir(os.path.join(fullpath,file)),all)
			files.sort()
		dirs=None
		if showDirs:
			dirs=filter(lambda dir: dir not in files,all)
		ret=[]
		if len(files)==0:
			o=Object()
			o.error="dirEmpty"
			return o
		path=conf["path"]
		if dirs:
			for i in dirs:
				o=Object()
				o.name=i
				o.path=path
				o.type="dir"
				ret.append(o)
		if files and not onlyDirs:
			for i in files:
				o=Object()
				o.name=i
				o.path=path
				#TODO change it to mimetype
				#o.type="file"
				ret.append(o)
		return List(ret)

	def tree(self,acenv,conf):
		#TODO as list but should return whole dir tree. Subdirs should be in subnodes of Object()
		pass

	def create(self,acenv,conf,update=False):
		D=acenv.doDebug
		#path=os.path.join(self.abspath+conf["path"])
		o=Object()
		if not update and os.path.isfile(conf["fullpath"]):
			o.status="error"
			o.error="fileExists"
			return o
		# path is a list eg /a/b/c/foo.xml -> ['a', 'b', 'c']
		path=os.path.normpath(conf["path"]).split("/")[:-1]
		currPath=self.abspath
		for d in path:
			currPath=os.path.join(currPath, d)
			if not os.path.isdir(currPath):
				os.mkdir(currPath)
		try:
			file=open(conf["fullpath"], 'w')
			#XXX this replace is pretty lame, need to investigate where the hell this \r is from, and do it cross-platform.
			file.write(conf["content"])#.replace("\r\n","\n"))
		except (IOError,OSError) ,e:
			o.status="error"
			o.error=e
			return o
		#FIXME - else or finally or smth else?
		else:
			file.close()
		return o

	def update(self,acenv,conf):
		return self.create(acenv,conf,True)

	def append(self,acenv,conf):
		D=acenv.doDebug
		path=acenv,conf["fullpath"]
		try:
			file=open(path, 'a')
			file.write(conf['content'])#.replace("\r\n","\n")
		except IOError,e:
			raise Error("IOError", 'cannot open %s'%(e))
		else:
			file.close()
		return Object()

	def delete(self,acenv,conf):
		D=acenv.doDebug
		path=self.abspath+replaceVars(acenv,conf["path"])
		if (os.path.exists(path)):
			if (os.path.isfile(path)):
				os.remove(path)
			else:
				shutil.rmtree(path)
		return Object()

	def copy(self,acenv,conf):
		#D=acenv.doDebug
		copyFrom=os.path.join(self.abspath,*replaceVars(acenv,conf["from"]).split("/"))
		copyTo=os.path.join(self.abspath,*replaceVars(acenv,conf["to"]).split("/"))
		if os.path.isfile(copyFrom) and not os.path.isfile(copyTo):
			shutil.copyfile(copyFrom, copyTo)
		return Object()

	def move(self,acenv,conf):
		copyFrom=os.path.join(self.abspath,*replaceVars(acenv,conf["from"]).split("/"))
		copyTo=os.path.join(self.abspath,*replaceVars(acenv,conf["to"]).split("/"))
		if os.path.isfile(copyFrom) and not os.path.isfile(copyTo):
			shutil.move(copyFrom, copyTo)
		return o

	def exists(self,acenv,conf):
		o=Object()
		o.exists=os.path.exists(conf["fullpath"])
		return o

	def get(self,acenv,conf):
		fullpath=conf["fullpath"]
		try:
			file=open(fullpath,"r")
			content=file.read()
		except IOError,e:
			#FIXIT
			raise e
			#print 'cannot open', conf["path"]
		else:
			file.close()
		o=Object()
		o.set("<![CDATA["+content.replace("]]>","]]>]]&gt;<![CDATA[")+"]]>")
		o._doFn=False
		return o

	def generate(self, acenv, config):
		D=acenv.doDebug
		if D:
			acenv.info("Component: 'FS'")
			acenv.info("Executing command: '%s'", config["command"])
		c=config["params"]
		conf={}
		for i in c:
			conf[i]=replaceVars(acenv, c[i])
		if D:
			if not conf.get("path"):
				acenv.error("path not suplied")
			elif conf["path"][0]!='/':
				acenv.error("missning '/' character at the begginig of 'path' attribute")
		try:
			conf["content"]=replaceVars(acenv,config["content"])
		except:
			pass
		conf["fullpath"]=os.path.join(self.abspath,*conf["path"].split("/"))
		return self.__getattribute__(config["command"])(acenv,conf)

	def parseAction(self, conf):
		if conf["command"] not in ("list", "create", "update", "append", "delete", "copy", "move", "exists", "get"):
			raise Error("Command '%s' do not exist!", config["command"])
		ret={
			"command":conf["command"]
		}
		if conf["content"]:
			s=[]
			for elem in conf["content"]:
				if type(elem) is tuple:
					s.append(tree2xml(elem))
				elif type(elem) is str:
					s.append(elem)
			ret["content"]=prepareVars("\n".join(s))
		ret["params"]=conf["params"]
		return ret

def getObject(config):
	return FileSystem(config)
