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

from ACR import acconfig
from ACR.errors import *
from ACR.utils import replaceVars,prepareVars
from ACR.components import *
from ACR import db
import time
import re
import locale

#re.I is case-insensitive regular expression
RE_CACHE=re.compile("insert|update|select|delete",re.I)

class DataBase(Component):
	def __init__(self,config):
		self.CONNECTIONS={}
		#if D: log.debug("Instance created with config=%s",config)
		#should implement lazy db connections
		if not config:
			raise Exception("database config not found.")
		self.config=config
		for i in config:
			attrs=i[1]
			cfg={
				"dbms":attrs.get("dbms","pgsql"),
				"dbname":attrs.get("name","default")
			}
			for node in i[2]:
				cfg[node[0]]="".join(node[2]).strip()
			conn=db.get(cfg)
			#conn.query("SET CLIENT_ENCODING TO '%s'"%(locale.normalize(config["lang"]+".UTF8")))
			self.CONNECTIONS[attrs.get("name","default")]=conn
			if attrs.get("default",False):#attrs["default"] is True or False or is not set
				self.CONNECTIONS["default"]=conn

	def determineQueryType(self,q):
		#if D: log.debug("started with q=%s",q)
		rs=RE_CACHE.search(q)
		return q[rs.start():rs.end()].lower()

	#data is list of complex values
	def evaluateMR(self,env,query,data):
		D=env.doDebug
		if D: env.dbg("start with query='%s' and data=%s",query,data)
		#dt=self.determineDataType(data)
		qt=self.determineQueryType(query)
		if D: env.dbg("determineQueryType returned with '%s'",qt)
		q=[]
		data=data[0]
		if qt=="insert":
			if D: env.dbg("detected insert")
			for i in data[1]:
				q.append(re.sub("{\$"+data[0]+"}",db.escapeString(i),query))
		elif qt=="update":
			#if D: env.warning("Update not implemented yet.")
			return query
		elif qt=="select":
			#if D: env.warning("Select not implemented yet.")
			return query
		elif qt=="update":
			#if D: env.warning("Delete not implemented yet.")
			return query
		else:
			if D: env.warning("Query type not detected. Returning unchanged SQL.")
			return query
		return ";".join(q)

	def generate(self,acenv,conf):
		if type(conf["query"]) is list:
			try:
				conf["query"]="".join(conf["query"])
			except:
				conf["query"]="".join(map(str,conf["query"]))
		return self.__getattribute__(conf["command"].split(":").pop())(acenv,conf)

	def none2null(self,s):
		if s.lower()=="none":
			return "null"
		return s

	def colaslist(self,env,conf):
		query=replaceVars(env,conf["query"],self.none2null)
		result=self.CONNECTIONS[conf.get("server","default")].query(query)
		ret=[]
		for i in result["rows"]:
			ret.append(i[0])
		return ret

	def query(self,env,conf):
		D=env.doDebug
		P=env.doProfiling
		if D: env.debug("START DB:query with: conf='%s'",conf)
		query=replaceVars(env,conf["query"],self.none2null)
		if type(query) is list:
			query="".join(map(str,query))
		if D: env.debug("replaceVars returned '%s'",query)
		if P:
			t=time.time()
		result=self.CONNECTIONS[conf.get("server","default")].query(query)
		if P:
			env.profiler["dbtimer"]+=time.time()-t
			env.profiler["dbcounter"]+=1
		if D: env.debug("database returned %s",result)
		if result and len(result["rows"]):
			if D: env.debug("Creating list of ordered dicts.")
			#TODO get relations keys and return them as attributes
			first=True #for debugging purposes
			ret=[]
			fields=result["fields"]
			cdata=conf["cdata"]
			for row in result["rows"]:
				r={}
				#TODO optimize returning row and value
				for i in xrange(len(row)):
					if type(row[i]) is str and fields[i] in cdata:
						s="<![CDATA["+row[i].replace("]]>","]]>]]&gt;<![CDATA[")+"]]>"
					else:
						s=row[i]
					r[fields[i]]=s
					#nodes.append((fields[i],s))
				first=False
				ret.append(r)
			if not conf["return"]=="list" and len(ret) is 1:
				#row
				if D:env.debug("END DB:query with one row: %s",ret[0])
				return ret[0]
				#if len(ret[2]) is 1:
					#value
				#	return Object(ret[2][0][2][0])
			else:
				if D:env.debug("END DB:query with multiple rows: %s",ret)
				return ret
		else:
			if D:env.debug("END DB:query with no rows.")
			return {}
		return ret

	#parses one action config which is passed to object
	def parseAction(self,conf):
		query=""
		for node in conf["content"]:
			if type(node) is str:
				query=str(" ".join(node.split()))
		params=conf["params"]
		return {
			"query":prepareVars(query.strip()),
			"server":params.get("server", "default"),
			"return":params.get("return"),
			"command":conf["command"],
			#TODO change it to re.strip
			"cdata":map(str.strip,params.get("cdata","").split(","))
		}

def getObject(config):
	return DataBase(config)
