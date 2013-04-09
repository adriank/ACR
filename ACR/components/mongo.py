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

"""
This component is pretty lame, because we translate text to python objects, sent them to pymongo which converts it back to the pretty same text representation as the input data. We do it for the sake of simplicity and security, but we are not happy with the result.

TODO:
- make component work also with one database using subcollections eg. rather than using db.database.collection, using db.oneDB.rootColl,collection. It saves space and the security layer is here so we don't need to rely on Mongo's own approach to users.
"""

from ACR.utils import replaceVars,prepareVars, str2obj, dicttree
from ACR.components import *
from ACR.utils.xmlextras import tree2xml
from xml.sax.saxutils import escape,unescape
import pymongo
from bson import objectid
from ACR.utils.interpreter import makeTree
import time

STR_TYPES=(str,unicode)

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
		try:
			return coll.update(where,o,safe=True,multi=True)
		except pymongo.errors.OperationFailure,e:
			return {
				"status":"error",
				"error":"NotUpdated",
				"message":str(e)
			}

	def insert(self,acenv,config):
		D=acenv.doDebug
		params=config["params"]
		coll=acenv.app.storage[params.get("coll",self.DEFAULT_COLL)]
		o=config["content"].execute(acenv)
		if D: acenv.debug("doing %s",coll.insert)
		try:
			id=coll.insert(o,safe=True)
		except Exception,e:
			return {
				"@status":"error",
				"@error":str(x.__class__.__name__),
				"@message":str(e)
			}
		if D:acenv.info("inserted: %s",o)
		ret={"@id":id,"@status":"ok"}
		#leaving space for debugging and profiling info
		return ret

	def save(self,acenv,config):
		D=acenv.doDebug
		if D: acenv.debug("START Mongo.save with: %s", config)
		params=config["params"]
		coll=acenv.app.storage[params.get("coll",self.DEFAULT_COLL)]
		o=config["content"].execute(acenv)
		if D: acenv.debug("doing %s",coll.insert)
		id=coll.save(o,safe=True)
		if D:acenv.debug("saved:\n%s",o)
		ret={"@id":id}
		#leaving space for debugging and profiling info
		return ret

	def remove(self,acenv,config):
		D=acenv.doDebug
		if D: acenv.debug("START Mongo.remove with: %s", config)
		params=config["params"]
		coll=acenv.app.storage[params.get("coll",self.DEFAULT_COLL)]
		o=config["content"].execute(acenv)
		if D: acenv.debug("doing %s",coll.insert)
		if o:
			lastError=coll.remove(o,safe=True)
		else:
			return {
				"@status":"error",
				"@error":"DataNotRemoved",
				"@message":"Empty object results in removal of all data. For safety this functionality is blocked here, please use removeAll command instead."
			}
		if D and not lastError:acenv.debug("removed:\n%s",o)
		#leaving space for debugging and profiling info
		return lastError or {"status":"ok"}

	def removeAll(self,acenv,config):
		D=acenv.doDebug
		if D: acenv.debug("START Mongo.removeAll with: %s", config)
		lastError=coll.remove({},safe=True)
		if D and not lastError:acenv.debug("removed:\n%s",o)
		#leaving space for debugging and profiling info
		return lastError or {"status":"ok"}

	def count(self,acenv,config):
		return self.find(acenv,config,count=True)

	def findOne(self,acenv,config):
		return self.find(acenv,config,one=True)

	def find(self,acenv,config,count=False,one=False):
		D=acenv.doDebug
		P=acenv.doProfiling
		params=config["params"]
		coll=acenv.app.storage[params.get("coll",self.DEFAULT_COLL)]
		p={
			"spec":params.get("where", config["content"]).execute(acenv)
		}
		if D:acenv.debug("Finding objects matching:\n%s",p["spec"])
		for i in params:
			#FIXME lame exception
			if type(params[i]) is list and i!='sort':
				params[i]=replaceVars(acenv,params[i])
		try:
			p["fields"]=params["fields"]
		except: pass
		if not one:
			try:
				p["skip"]=int(params["skip"])
			except: pass
			try:
				p["limit"]=int(params["limit"])
			except: pass
			try:
				p["sort"]=params["sort"]
			except:
				pass
		if P: t=time.time()
		if count:
			ret=coll.find(**p).count()
			if D:acenv.debug("Objects matching count is: %s",ret)
		elif one:
			ret=list(coll.find(**p).limit(-1))
			ret=ret and ret[0] or None
		else:
			ret=list(coll.find(**p))
			if ret and params.has_key("sort") and len(params["sort"]) is 1:
				sortBy=params['sort'][0][0]
				if ret[0].has_key(sortBy)\
				and type(ret[0][sortBy]) in STR_TYPES\
				or ret[-1].has_key(sortBy)\
				and type(ret[-1][sortBy]) in STR_TYPES:
					if D:acenv.debug("Doing additional Python sort")
					def sortedKey(k):
						try:
							return k[sortBy].lower()
						except:
							return ''
					pars={"key":sortedKey}
					if params['sort'][0][1] is pymongo.DESCENDING:
						pars["reverse"]=True
					ret=sorted(ret, **pars)
		if P:
			acenv.profiler["dbtimer"]+=time.time()-t
			acenv.profiler["dbcounter"]+=1
		if ret:
			#if len(ret) is 1:
			#	if D:acenv.debug("END Mongo.find with %s",ret[0])
			#	return ret[0]
			if D:acenv.debug("END Mongo.find with %s",ret)
			return ret
		else:
			if count:
				if D:acenv.debug("END Mongo.count with 0")
				return ret
			if D:acenv.debug("END Mongo.find with no object")
			return {"@status":"noData"}

	def generate(self, acenv,config):
		D=acenv.doDebug
		if D: acenv.debug("START Mongo:%s with %s",config["command"].split(":").pop(), config)
		db=acenv.app.storage
		params=config["params"]
		collName=params.get("coll",self.DEFAULT_COLL)
		if type(collName) in (str,unicode):
			coll=acenv.app.storage[collName]
		coll=dicttree.get(acenv.app.storage,params.get("coll",self.DEFAULT_COLL))
		return self.__getattribute__(config["command"].split(":").pop())(acenv,config)

	def parseAction(self,config):
		s=[]
		fields={}
		pars=config["params"]
		for elem in config["content"]:
			if type(elem) is tuple:
				if elem[0]=="where":
					pars["where"]=makeTree("".join(elem[2]))
				elif elem[0]=="field":
					fields[elem[1]["name"]]=bool(str2obj(elem[1]["show"]))
				else:
					pars[elem[0]]=(elem[1],elem[2])
			elif type(elem) is str:
				s.append(elem.strip())
		try:
			coll=pars["coll"].split(".")
			if len(coll) is 1:
				coll=coll[0]
			pars["coll"]=coll
		except KeyError:
			raise Error("no coll parameter specified")
		try:
			sort=pars["sort"].split(",")
			directions=pars.get("direction",self.DIRECTION).split(",")
			directions=map(lambda x: pymongo.__dict__.get(x.upper()),directions)
			if len(directions)>=len(sort):
				pars["sort"]=zip(sort,directions)
			else:
				import itertools
				pars["sort"]=list(itertools.izip_longest(sort,directions,fillvalue=directions[-1]))
		except:
			pass
		if fields:
			pars["fields"]=fields
		return {
			"command":config["command"],
			"content":makeTree("".join(s)),
			"params":pars
		}

def getObject(config):
	return Mongo(config)
