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
from ACF.utils.xmlextras import tree2xml#,str2obj
import os
import shutil
import fnmatch

class FileSystem(Component):
	def __init__(self,config):
		#self.config=config
		#TODO check whether it is path to proper directory (exists, permissions etc) or not
		self.path=config[0][2][0]

	def list(self,acenv,conf):
		path=self.path+conf["path"]
		showDirs=conf.get("showdirs",True)
		_filter=conf.get("filter","")
		files=os.listdir(path)
		if not showDirs:
			files=filter(lambda file: not os.path.isdir(os.path.join(path,file)),files)
		if _filter:
			files=filter(lambda file: fnmatch.fnmatch(file, _filter),files)
		ret=[]
		if len(files)==0:
			return ("object",{"status":"ok","code":"dirEmpty"},None)
		for i in files:
			ret.append(("object",{"name":i},None))
		if len(ret)==1:
			ret=ret[0]
			ret[1]["status"]="ok"
		return ret

	def create(self,acenv,conf):
		path=os.path.join(self.path+conf["path"])
		#TODO if whole path do not exist -> create all dirs in path
		if (os.path.isfile(path)):
			return ("object",{"status":"error","code":"fileExists"},None)
		try:
			file = open(path, 'w')
			file.write(conf["content"])
		except IOError,e:
			return ("object",{"status":"error","code":"IOError"},e)
		else:
			file.close()
		return ("object",{"status":"ok"},None)

	def update(self,acenv,conf):
		path=self.path+replaceVars(acenv,conf["path"])
		content=replaceVars(acenv,conf["content"])
		try:
			file = open(path, 'w')
			file.write(content)
		except IOError:
			print 'cannot open', path
		else:
			file.close()
		return ("object",{"status":"ok"},None)

	def append(self,acenv,conf):
		path=self.path+replaceVars(acenv,conf["path"])
		content=replaceVars(acenv,conf["content"])
		try:
			file = open(path, 'a')
			file.write(content)
		except IOError:
			print 'cannot open', path
		else:
			file.close()
		return ("object",{"status":"ok"},None)

	def delete(self,acenv,conf):
		path=self.path+replaceVars(acenv,conf["path"])
		if (os.path.exists(path)):
			if (os.path.isfile(path)):
				os.remove(path)
			else:
				shutil.rmtree(path)
		return ("object",{"status":"ok"},None)

	def copy(self,acenv,conf):
		copyFrom=self.path+replaceVars(acenv,conf["from"])
		copyTo=self.path+replaceVars(acenv,conf["to"])
		if (os.path.isfile(copyFrom)):
			shutil.copyfile(copyFrom, copyTo)
		return ("object",{"status":"ok"},None)

	def move(self,acenv,conf):
		copyFrom=self.path+replaceVars(acenv,conf["from"])
		copyTo=self.path+replaceVars(acenv,conf["to"])
		if (os.path.isfile(copyFrom)):
			shutil.move(copyFrom, copyTo)
		return ("object",{"status":"ok"},None)

	def exists(self,acenv,conf):
		path=self.path+replaceVars(acenv,conf["path"])
		return ("object",{"exists":os.path.isfile(path)},[])

	def get(self,acenv,conf):
		path=self.path+replaceVars(acenv,conf["path"])
		try:
			file=open(path,"r")
			content=file.read()
		except IOError:
			print 'cannot open', path
		else:
			file.close()
		return ("object",{"status":"ok"},[content])

	def generate(self, acenv, config):
		conf={}
		for i in config:
			if type(config[i]) is str:
				conf[i]=replaceVars(acenv,config[i])
			else:
				conf[i]=config[i]
		return self.__getattribute__(conf["command"])(acenv,conf)

	def parseAction(self, conf):
		ret={"command":conf["command"]}
		ret.update(conf["params"])
		if conf["content"]:
			s=[]
			for elem in conf["content"]:
				if type(elem) is tuple:
					s.append(tree2xml(elem)+"\n")
				elif type(elem) is str:
					s.append(elem+"\n")
			ret["content"]="".join(s)
		return ret

def getObject(config):
	return FileSystem(config)
