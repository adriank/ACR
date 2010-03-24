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
			print "dupa jasiu ", i, "dalej", i[2][0]
	
			
	def generate(self, acenv, conf):
		print "generate: ",conf
		#return self.__getattribute__(conf["do"].split(":").pop())(acenv,conf)
		
	def parseAction(self, root):
		operation=root[0].split(':')[1]
				
		if operation=="list":
			print "list"
		elif operation=="add":
			print "add"
		elif operation=="set":
			print "set"
		elif operation=="create":
			if (os.path.isfile(root[1]["path"])):
				raise os.error, "File exist"
			else:
				try:
					file = open(root[1]["path"], 'w')
					file.write(root[2][0])
				except IOError:
					print 'cannot open', root[1]["path"]
				else:
					file.close()
			print "jest create"
		elif operation=="update":
			if (os.path.isfile(root[1]["path"])):
				try:
					file = open(root[1]["path"], 'w')
					file.write(root[2][0])
				except IOError:
					print 'cannot open', root[1]["path"]
				else:	
					file.close()
			else:
				raise os.error, "File not exist"
			print "jest update"
		elif operation=="append":
			if (os.path.isfile(root[1]["path"])):
				try:
					file = open(root[1]["path"], 'a')
					file.write(root[2][0])
				except IOError:
					print 'cannot open', root[1]["path"]
				else:	
					file.close()
			else:
				raise os.error, "File not exist"
			
		elif operation=="delete":
			if (os.path.isfile(root[1]["path"])):
				os.remove(root[1]["path"])
			
		elif operation=="copy":
			if (os.path.isfile(root[1]["from"]) and os.path.isfile(root[1]["to"])):
				shutil.copyfile(root[1]["from"], root[1]["to"])
				
		elif operation=="move":
			if (os.path.isfile(root[1]["from"]) and os.path.isfile(root[1]["to"])):
				shutil.move(root[1]["from"], root[1]["to"])
				
			
		elif operation=="exists":
			if (os.path.isfile(root[1]["path"])):
				print "File exist"
			else:
				print "File not exist"
		elif operation=="get":
			if (os.path.isfile(root[1]["path"])):
				try:
					file=open(root[1]["path"],"r")
					content=file.read()
					
				except IOError:
					print 'cannot open',root[1]["path"]
				else:	
					file.close()
					return ("object",{},[content])
			
		ret=root[1].copy()
		ret["do"]=root[0]
		return ret
	
def getObject(config):
	return file(config)
