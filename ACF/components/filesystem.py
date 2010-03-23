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
from ACF.components.base import Component
from ACF.errors import *
from ACF.utils.xmlextras import dom2tree
from ACF.utils import replaceVars
import os
templateDir="/home/templates/"

class FileSystem(Component):
	def generate(self,data):
		path="/".join(globals.appDir.split("/")[0:-2])
		ret=[]
		for a in self.config["actions"]:
			if a[1]["path"].strip()[0]!="/":
				raise Error("pathNotAbsolute")
			dst=path+replaceVars(a[1]["path"])
			actionName=a[0].lower()
			if actionName=="create":
				if os.path.exists(dst):
					ret.append(("warning",{"code":"fileExists","name":replaceVars(a[1]["path"])},None))
					continue
				if a[1]["contentSource"]=="template":
					import shutil
					shutil.copyfile(templateDir+a[1]["templateName"],dst)
					stat=os.stat("/home/"+globals.appDomain.replace(".","_"))[4:6]
					os.chown(dst, stat[0], stat[1])
				#else:
				#	s=replaceVars(a[2][0])
			elif actionName=="list":
				for i in os.listdir(path):
					raise os.path.basename()
						#ret.append(("file",i[0:-4]))
		if len(ret)>0:
			return ret
		else:
			return None

def parseConfig(root):
	r=dom2tree(root)[2]
	conditions=[]
	actions=[]
	for elem in r:
		if elem[0].lower()=="conditions":
			for e in elem[2]:
				conditions.append(e)
		else:
			actions.append(elem)
	return {
		"conditions":conditions,
		"actions":actions
	}

def getObject(config):
	return FileSystem(config)
