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

from ACR.utils import replaceVars,prepareVars
from ACR.components import *
from ACR.utils.xmlextras import tree2xml
from xml.sax.saxutils import escape,unescape
import pymongo
import json

EMPTY_OBJECT=Object()

class Mongo(Component):
	SERVER='localhost'
	PORT=27017
	def __init__(self,config):
		if not config:
			config={}
		server=config.get("server",self.SERVER)
		port=config.get("port",self.PORT)
		self.conn=pymongo.Connection(server,port)
		self.DEFAULT_DB=config.get("defaultdb")
		self.DEFAULT_COLL=config.get("defaultcoll")

	def insert(self,acenv,config):
		params=config["params"]
		coll=self.conn[params.get("db",self.DEFAULT_DB)][params.get("coll",self.DEFAULT_COLL)]
		coll.insert(json.loads(replaceVars(acenv,config["content"])))
		return EMPTY_OBJECT

	def find(self,acenv,config):
		params=config["params"]
		coll=self.conn[params.get("db",self.DEFAULT_DB)][params.get("coll",self.DEFAULT_COLL)]
		prototype=replaceVars(acenv,params.get("prototype", config["content"]))
		ret=list(coll.find(json.loads(prototype), params.get("fields")))
		if ret:
			if len(ret) is 1:
				return ret[0]
			return ret
		else:
			return {}

	def generate(self, acenv,config):
		return self.__getattribute__(config["command"].split(":").pop())(acenv,config)

	def parseAction(self,config):
		s=[]
		fields={}
		pars=config["params"]
		for elem in config["content"]:
			if type(elem) is tuple:
				if elem[0]=="prototype":
					pars["prototype"]="".join(elem[2])
				elif elem[0]=="field":
					fields[elem[1]["name"]]=int(elem[1]["show"])
				else:
					pars[elem[0]]=(elem[1],elem[2])
			elif type(elem) is str:
				s.append(elem.strip())
		if fields:
			pars["fields"]=fields
		return {
			"command":config["command"],
			"content":prepareVars("".join(s)),
			"params":pars
		}

def getObject(config):
	return Mongo(config)
