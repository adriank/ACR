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

from ACR.utils import replaceVars,prepareVars, str2obj
from ACR.components import *
from ACR.utils.xmlextras import tree2xml
from xml.sax.saxutils import escape,unescape
import pymongo
from bson import objectid
from ACR.utils.interpreter import make_tree
import time

class Mongo(Component):
	SERVER='localhost'
	PORT=27017
	DIRECTION="DESCENDING"
	def __init__(self,config):
		if not config:
			config={}
		server=config.get("server",self.SERVER)
		port=config.get("port",self.PORT)
		#self.conn=pymongo.Connection()
		#self.DEFAULT_DB=config.get("defaultdb")
		self.DEFAULT_COLL=config.get("defaultcoll")

	def update(self,acenv,config):
		D=acenv.doDebug
		params=config["params"]
		coll=acenv.app.storage[params.get("coll",self.DEFAULT_COLL)]
		where=params["where"].execute(acenv)
		o=config["content"].execute(acenv)
		if D:
			acenv.debug("where clause is %s",where)
			acenv.debug("update object is %s",o)
		coll.update(where,o,safe=True)

	def insert(self,acenv,config):
		D=acenv.doDebug
		params=config["params"]
		coll=acenv.app.storage[params.get("coll",self.DEFAULT_COLL)]
		o=config["content"].execute(acenv)
		if D: acenv.debug("doing %s",coll.insert)
		id=coll.insert(o,safe=True)
		if D:acenv.info("inserted: %s",o)
		ret={"@id":id,"@status":"ok"}
		#leaving space for debugging and profiling info
		return ret

	def save(self,acenv,config):
		D=acenv.doDebug
		if D: acenv.debug("START Mongo.save with: %s", config)
		params=config["params"]
		coll=acenv.app.storage[params.get("coll",self.DEFAULT_COLL)]
		o=json.loads(replaceVars(acenv,config["content"],fn=str),object_hook=object_hook)
		if D: acenv.debug("doing %s",coll.insert)
		id=coll.save(o,safe=True)
		if D:acenv.debug("saved:\n%s",o)
		ret={"@id":id}
		#leaving space for debugging and profiling info
		return ret

	def count(self,acenv,config):
		return self.find(acenv,config,count=True)

	def find(self,acenv,config,count=False):
		D=acenv.doDebug
		P=acenv.doProfiling
		params=config["params"]
		coll=acenv.app.storage[params.get("coll",self.DEFAULT_COLL)]
		#prototype=replaceVars(acenv,params.get("where", config["content"]),fn=str)
		p={"spec":params.get("where", config["content"]).execute(acenv)}
		for i in params:
			if type(params[i]) is list:
				params[i]=replaceVars(acenv,params[i])
		if params.has_key("fields"):
			p["fields"]=params["fields"]
		if params.has_key("skip"):
			p["skip"]=int(params["skip"])
		if params.has_key("limit"):
			p["limit"]=int(params["limit"])
		if params.has_key("sort"):
			dir=pymongo.__dict__.get(params.get("direction",self.DIRECTION).upper())
			p["sort"]=[(params["sort"],dir)]
		if P: t=time.time()
		if count:
			ret=coll.find(**p).count()
			#if D: acenv.debug("")
			return ret
		ret=list(coll.find(**p))
		if P:
			acenv.profiler["dbtimer"]+=time.time()-t
			acenv.profiler["dbcounter"]+=1
		if ret:
			if len(ret) is 1:
				if D:acenv.debug("END Mongo.find with %s",ret[0])
				return ret[0]
			if D:acenv.debug("END Mongo.find with %s",ret)
			return ret
		else:
			if D:acenv.debug("END Mongo.find with no object")
			return {"@status":"nodata"}

	def generate(self, acenv,config):
		D=acenv.doDebug
		if D: acenv.debug("START Mongo:%s with %s",config["command"].split(":").pop(), config)
		return self.__getattribute__(config["command"].split(":").pop())(acenv,config)

	def parseAction(self,config):
		s=[]
		fields={}
		pars=config["params"]
		for elem in config["content"]:
			if type(elem) is tuple:
				if elem[0]=="where":
					pars["where"]=make_tree("".join(elem[2]))
				elif elem[0]=="field":
					fields[elem[1]["name"]]=bool(str2obj(elem[1]["show"]))
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
			"content":make_tree("".join(s)),
			"params":pars
		}

def getObject(config):
	return Mongo(config)
