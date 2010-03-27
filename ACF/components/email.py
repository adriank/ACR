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


from ACF import globals
from ACF.utils import conditionchecker,mail,replaceVars
from ACF.components import Component
from ACF.utils.xmlextras import dom2tree
from ACF.errors import *

class email(Component):
	def handle(self,data):
		conf=self.config
		content=""
		if conf["content"][1] is not None and conf["content"][1].has_key("fromFile"):
			file=replaceVars(conf["content"]["fromFile"])
			try:
				f=open(globals.appDir+file,"r")
				content=f.read().decode("utf-8")
				f.close()
			except IOError,e:
				raise Error("fileNotFound",str(e))
		else:
			content=conf["content"][2][0]
		conf["headers"]["Subject"]=replaceVars(conf["headers"]["Subject"])
		conf["headers"]["From"]=replaceVars(conf["headers"]["From"])
		conf["headers"]["To"]=replaceVars(conf["headers"]["To"])
		mail.send(conf["headers"],replaceVars(content))

def parseConfig(root):
	r=dom2tree(root)[2]
	conditions=[]
	headers={}
	content=None
	for elem in r:
		if elem[0].lower()=="conditions":
			for e in elem[2]:
				conditions.append(e)
		elif elem[0].lower()=="headers":
			for i in elem[1]:
				headers[i.capitalize()]=elem[1][i]
		elif elem[0].lower()=="content":
			content=elem
	try:
		_from=headers["Fromadress"]
	except KeyError:
		raise Error("fromAdressNotExist", "headers should have fromAdress attribute")
	if headers.has_key("Fromname"):
		_from=headers["Fromname"]+" <"+headers["Fromadress"]+">"
	try:
		del(headers["Fromname"], headers["Fromadress"])
	except Exception:
		pass
	headers["From"]=_from
	return {
		"conditions":conditions,
		"content":content,
		"headers":headers
	}

def getObject(config):
	return email(config)
