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


from ACF import globals
from ACF.components import Component
from ACF.errors import *
from ACF.utils import replaceVars
from ACF.utils.xmlextras import tree2xml
import os
import shutil
name="file"
templateDir="/home/templates/"

class file(Component):
	def __init__(self,config):
		self.config=config
		for i in config:
			path=i[2][0]
			self.path=path
	
	def list(self,acenv,conf):
		for i in os.listdir(conf["path"]):
			print i
		return ("object",{"status":"ok"},None)	
	
	def create(self,acenv,conf):
		if (os.path.isfile(conf["path"])):
			raise os.error, "File exist"
		else:
			file = open(conf["path"], 'w')
			file.write(conf["content"])
			file.close()
		return ("object",{"status":"ok"},None)

	def update(self,acenv,conf):
		if (os.path.isfile(conf["path"])):
			file = open(conf["path"], 'w')
			file.write(conf["content"])
			file.close()
		else:
			raise os.error, "File not exist"
		return ("object",{"status":"ok"},None)

	def append(self,acenv,conf):
		if (os.path.isfile(conf["path"])):
			file = open(conf["path"], 'a')
			file.write(conf["content"])
			file.close()
		else:
			raise os.error, "File not exist"
		return ("object",{"status":"ok"},None)

	def delete(self,acenv,conf):
		if (os.path.isfile(conf["path"])):
			os.remove(conf["path"])
		return ("object",{"status":"ok"},None)

	def copy(self,acenv,conf):
		if (os.path.isfile(conf["from"])):
			shutil.copyfile(conf["from"], conf["to"])
		return ("object",{"status":"ok"},None)

	def move(self,acenv,conf):
		if (os.path.isfile(conf["from"])):
			shutil.move(conf["from"], conf["to"])
		return ("object",{"status":"ok"},None)

	def exists(self,acenv,conf):
		if (os.path.isfile(conf["path"])):
			exists="true"
		else:
			exists="false"
		print "File exist: ", exists
		return ("object",{},[exists])

	def get(self,acenv,conf):
		if (os.path.isfile(conf["path"])):
			file=open(conf["path"],"r")
			content=file.read()
			print content
			file.close()
			return ("object",{},[content])
		
		
		
	def generate(self, acenv, conf):
		return self.__getattribute__(conf["do"].split(":").pop())(acenv,conf)
		
	def parseAction(self, root):
		print "root: ",root	
		ret=root[1].copy()
		ret["do"]=root[0]
		if root[2]:
			s=[]
			for elem in root[2]:
				if type(elem) is tuple:
					s.append(tree2xml(elem))
				elif type(elem) is str:
					s.append(elem)
			ret["content"]="".join(s)
			print "ret: ",ret
		return ret
	
def getObject(config):
	return file(config)
