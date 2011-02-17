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
import time
from pymongo.json_util import object_hook

class Mongo(Component):
	SERVER='localhost'
	PORT=27017
	def __init__(self,config):
		if not config:
			config={}
		server=config.get("server",self.SERVER)
		port=config.get("port",self.PORT)
		self.conn=pymongo.Connection()
		self.DEFAULT_DB=config.get("defaultdb")
		self.DEFAULT_COLL=config.get("defaultcoll")

	def update(self,acenv,config):
		D=acenv.doDebug
		params=config["params"]
		coll=acenv.app.storage[params.get("coll",self.DEFAULT_COLL)]
		where=json.loads(replaceVars(acenv,params["where"]),object_hook=object_hook)
		o=json.loads(replaceVars(acenv,config["content"]),object_hook=object_hook)
		print where
		print o
		coll.update(where,o)

	def insert(self,acenv,config):
		D=acenv.doDebug
		params=config["params"]
		coll=acenv.app.storage[params.get("coll",self.DEFAULT_COLL)]
		id=coll.insert(json.loads(replaceVars(acenv,config["content"])))
		if D:acenv.debug("inserted:\n%s",replaceVars(acenv,config["content"]))
		ret={"@id":id}
		#leaving space for debugging and profiling info
		return ret

	def find(self,acenv,config):
		params=config["params"]
		coll=acenv.app.storage[params.get("coll",self.DEFAULT_COLL)]
		prototype=replaceVars(acenv,params.get("where", config["content"]))
		p={"spec":json.loads(prototype)}
		if params.has_key("fields"):
			p["fields"]=params["fields"]
		if params.has_key("skip"):
			p["skip"]=int(params["skip"])
		if params.has_key("limit"):
			p["limit"]=int(params["limit"])
		q={"_id" : pymongo.objectid.ObjectId("4d4f04a9ba060531ef000000")}
		t=time.time()
		ret=list(coll.find(**p))
		#print round((time.time()-t)*1000,5)
		if True or D:
			acenv.dbg["dbtimer"]+=time.time()-t
		if ret:
			if len(ret) is 1:
				return ret[0]
			return ret
		else:
			return {"@status":"nodata"}

	def generate(self, acenv,config):
		return self.__getattribute__(config["command"].split(":").pop())(acenv,config)

	def parseAction(self,config):
		s=[]
		fields={}
		pars=config["params"]
		for elem in config["content"]:
			if type(elem) is tuple:
				if elem[0]=="where":
					pars["where"]=prepareVars("".join(elem[2]))
				elif elem[0]=="field":
					fields[elem[1]["name"]]=int(elem[1]["show"])
				else:
					pars[elem[0]]=(elem[1],elem[2])
			elif type(elem) is str:
				s.append(elem.strip())
		if not pars.has_key("coll"):
			raise Error("no coll parameter specified")
		if fields:
			pars["fields"]=fields
		return {
			"command":config["command"],
			"content":prepareVars("".join(s)),
			"params":pars
		}

def getObject(config):
	return Mongo(config)
