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

from ACF.components import *
from ACF.errors import *
from ACF.utils import replaceVars
from ACF.utils.xmlextras import tree2xml#,str2obj
import os
import shutil
import fnmatch

D=True

class FileSystem(Component):
	def __init__(self,config):
		#self.config=config
		#TODO check whether it is path to proper directory (exists, permissions etc) or not
		self.path=config[0][2][0]

	def list(self,acenv,conf):
		l=Object()
		path=conf["path"]
		showDirs=conf.get("showdirs",True)
		_filter=conf.get("filter","")
		files=os.listdir(conf["path"])
		if not showDirs:
			files=filter(lambda file: not os.path.isdir(os.path.join(path,file)),files)
		else:
			if D: acenv.warning("'list' has bad value: showDirs=%s", showDirs)
		if _filter:
			files=filter(lambda file: fnmatch.fnmatch(file, _filter),files)
		if conf.get("extension","")=="hide":
			files=map(lambda f:	os.path.splitext(f)[0],files)
		files.sort()
		ret=[]
		if len(files)==0:
			l.status="ok"
			l.code="dirEmpty"
			return l #return ("object",{"status":"ok","code":"dirEmpty"},None)
		for i in files:
			l=Object()
			l.name=i
			ret.append(l) #ret.append(("object",{"name":i},None))
		if len(ret)==1:
			ret[0].status="ok"
			#ret=ret[0]
			#ret[1]["status"]="ok"
		return List(ret)

	def create(self,acenv,conf,update=False):
		#path=os.path.join(self.path+conf["path"])
		#TODO if whole path do not exist -> create all dirs in path
		cr=Object()
		if not update and os.path.isfile(conf["path"]):
			cr.status="error"
			cr.code="fileExists"
			return cr #return ("object",{"status":"error","code":"fileExists"},None)
		try:
			file = open(conf["path"], 'w')
			#XXX this replace is pretty lame, need to investigate where the hell this \r is from, and do it cross-platform.
			file.write(conf["content"].replace("\r\n","\n"))
		except IOError,e:
			cr.status="error"
			cr.code="IOError"
			return cr #return ("object",{"status":"error","code":"IOError"},e)
		else:
			file.close()
		cr.status="ok"	
		return cr #return ("object",{"status":"ok"},None)

	def update(self,acenv,conf):
		return self.create(acenv,conf,True)

	def append(self,acenv,conf):
		ap=Object()
		path=self.path+replaceVars(acenv,conf["path"])
		content=replaceVars(acenv,conf["content"])
		try:
			file = open(path, 'a')
			file.write(content.replace("\r\n","\n"))
		except IOError:
			print 'cannot open', path
		else:
			file.close()
		ap.status="ok"	
		return ("object",{"status":"ok"},None)

	def delete(self,acenv,conf):
		dl=Object()
		path=self.path+replaceVars(acenv,conf["path"])
		if (os.path.exists(path)):
			if (os.path.isfile(path)):
				os.remove(path)
			else:
				shutil.rmtree(path)
		dl.status="ok"		
		return dl #return ("object",{"status":"ok"},None)

	def copy(self,acenv,conf):
		cp=Object()
		copyFrom=self.path+replaceVars(acenv,conf["from"])
		copyTo=self.path+replaceVars(acenv,conf["to"])
		if (os.path.isfile(copyFrom)):
			shutil.copyfile(copyFrom, copyTo)
		cp.status="ok"	
		return cp #return ("object",{"status":"ok"},None)

	def move(self,acenv,conf):
		mv=Object()
		copyFrom=self.path+replaceVars(acenv,conf["from"])
		copyTo=self.path+replaceVars(acenv,conf["to"])
		if (os.path.isfile(copyFrom)):
			shutil.move(copyFrom, copyTo)
		mv.status="ok"	
		return mv #return ("object",{"status":"ok"},None)

	def exists(self,acenv,conf):
		ex=Object()
		path=self.path+replaceVars(acenv,conf["path"])
		ex.exists=os.path.isfile(path)
		return ex #return ("object",{"exists":os.path.isfile(path)},[])

	def get(self,acenv,conf):
		g=Object()
		try:
			file=open(conf["path"],"r")
			content=file.read()
		except IOError,e:
			raise e
			print 'cannot open', conf["path"]
		else:
			file.close()
		g.status="ok"
		g.content="<![CDATA["+content.replace("]]>","]]>]]&gt;<![CDATA[")+"]]>"
		return g #return ("object",{"status":"ok"},["<![CDATA["+content.replace("]]>","]]>]]&gt;<![CDATA[")+"]]>"])

	def generate(self, acenv, config):
		if D:
			acenv.info("Component: 'FS'")
			acenv.info("Command: '%s'",replaceVars(acenv,config["command"]))
			if replaceVars(acenv,config["command"]) not in ("list", "create", "update", "append", "delete", "copy", "move", "exists", "get"):
				acenv.error("Command '%s' not exist!",replaceVars(acenv,config["command"]))
		conf={}
		for i in config:
			if type(config[i]) is str:
				conf[i]=replaceVars(acenv,config[i])
			else:
				conf[i]=config[i]
			if D:
				if i!= "command":acenv.dbg("attribute: '%s', value: '%s'", i, conf[i])
				
		if D:
			if not conf["path"]:
				acenv.warning("missning '/' character at the begginig of 'path' attribute")
			elif conf["path"][0] !=  '/':
				acenv.warning("missning '/' character at the begginig of 'path' attribute")
		conf["path"]=os.path.join(self.path+conf["path"])
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
