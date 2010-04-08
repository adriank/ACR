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
from ACF.errors import *
from ACF.utils import replaceVars,xmlextras
from ACF.components import Component, Generation
from ACF import db
import time
import re, logging

log=logging.getLogger('ACF.component.database')
d=logging.doLog
#re.I==case-insensitive
RE_CACHE=re.compile("insert|update|select|delete",re.I)

class DataBase(Component):
	CONNECTIONS={}#class variable, dont overwrite
	def __init__(self,config):
		if d: log.debug("Instance created with config=%s",config)
		#should implement lazy db connections
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
			self.CONNECTIONS[attrs.get("name","default")]=conn
			if attrs.get("default",False):#attrs["default"] is True or False or is not set
				self.CONNECTIONS["default"]=conn

	def determineQueryType(self,q):
		if d: log.debug("started with q=%s",q)
		rs=RE_CACHE.search(q)
		return q[rs.start():rs.end()].lower()

	#data is list of complex values
	def evaluateMR(self,env,query,data):
		if d: log.debug("start with query='%s' and data=%s",query,data)
		#dt=self.determineDataType(data)
		qt=self.determineQueryType(query)
		if d: log.debug("determineQueryType returned with '%s'",qt)
		q=[]
		data=data[0]
		if qt=="insert":
			if d: log.debug("detected insert")
			for i in data[1]:
				q.append(re.sub("{\$"+data[0]+"}",db.escapeString(i),query))
		elif qt=="update":
			if d: log.warning("Update not implemented yet.")
			return query
		elif qt=="select":
			if d: log.warning("Select not implemented yet.")
			return query
		elif qt=="update":
			if d: log.warning("Delete not implemented yet.")
			return query
		else:
			if d: log.warning("Query type not detected. Returning unchanged SQL.")
			return query
		return ";".join(q)

	def generate(self,env,actionConf):
		if d: log.debug("start with env=%s, actionConf=%s",env,actionConf)
		multiRequest=[]
		if d: log.debug("Doing escapeString on data")
		data=env.requestStorage.copy()
		for i in data:
			if d: log.info("Type of '%s' is '%s'",i,str(type(data[i]))[7:-2])
			if type(data[i]) is list:
				multiRequest.append((i,data[i]))
			else:
				data[i]=db.escapeString(str(data[i]))
		query=replaceVars(env,actionConf['query'])
		if d: log.debug("replaceVars returned '%s'",query)
		#query is filled with simple type data now
		if len(multiRequest)>0:
			if d: log.info("multirequest detected")
			query=self.evaluateMR(env,query,multiRequest)
			if d: log.debug("evaluateMR returned %s",query)
		else:
			if d: log.debug("multiRequest not needed")
		if d: log.info("Querying database with '%s'",query)
		if True: #env.debug:
			t=time.time()
		result=self.CONNECTIONS[actionConf.get("server","default")].query(query)
		if True: #env.debug:
			env.debug["dbtimer"]+=time.time()-t
		if d: log.debug("'query' returned %s",result)
		if result:
			if d: log.debug("Creating list of ordered dicts.")
			#TODO get relations keys and return them as attributes
			first=True #for debugging purposes
			ret=[]
			fields=result["fields"]
			for row in result["rows"]:
				nodes=[]
				#TODO optimize returning row and value
				for i in xrange(len(row)):
					#if col in actionConf["cdata"]:
					#	s="<![CDATA["+s.replace("]]>","]]>]]&gt;<![CDATA[")+"]]>"
					if d and first: log.info("'%s' appended as node",col)
					nodes.append((fields[i],None,[row[i]]))
				first=False
				ret.append(Generation(nodes))
			if len(ret) is 1:
				#row
				ret=ret[0]
				if len(ret[2]) is 1:
					#value
					return Generation(ret[2][0][2][0])
			else:
				return ret #("list",{},ret)
		else:
			return Generation()
		return ret

	#parses one action config which is passed to object
	def parseAction(self,conf):
		query=""
		for node in conf["content"]:
			if type(node) is str:
				query=str(" ".join(node.split()))
		return {
			"query":query,
			"server":conf["params"].get("server", "default"),
			"return":conf["params"].get("get","table")
		}

def getObject(config):
	return DataBase(config)
