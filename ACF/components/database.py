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
from ACF.components import *
from ACF import db
import time
import re, logging

#log=logging.getLogger('ACF.component.database')
#re.I==case-insensitive regular expression
RE_CACHE=re.compile("insert|update|select|delete",re.I)

class DataBase(Component):
	CONNECTIONS={}#class variable, dont overwrite
	def __init__(self,config):
		#if D: log.debug("Instance created with config=%s",config)
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
		#if D: log.debug("started with q=%s",q)
		rs=RE_CACHE.search(q)
		return q[rs.start():rs.end()].lower()

	#data is list of complex values
	def evaluateMR(self,env,query,data):
		D=env.debug
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

	def generate(self,env,actionConf):
		env.info("Component: 'DB'")
		D=env.debug
		if D: env.dbg("start with actionConf=%s",actionConf)
		multiRequest=[]
		if D: env.dbg("Doing escapeString on data")
		data=env.requestStorage.copy()
		for i in data:
			if D: env.info("Type of '%s' is '%s'",i,str(type(data[i]))[7:-2])
			if type(data[i]) is list:
				multiRequest.append((i,data[i]))
			else:
				data[i]=db.escapeString(str(data[i]))
		print multiRequest
		query=replaceVars(env,actionConf['query'])
		if D: env.dbg("replaceVars returned '%s'",query)
		#query is filled with simple type data now
		if len(multiRequest)>0:
			if D: env.info("multirequest detected")
			query=self.evaluateMR(env,query,multiRequest)
			if D: env.dbg("evaluateMR returned %s",query)
		else:
			if D: env.dbg("multiRequest not needed")
		if D: env.info("Querying database with '%s'",query)
		if True: #env.debug:
			t=time.time()
		result=self.CONNECTIONS[actionConf.get("server","default")].query(query)
		#if True: #env.debug:
		#	env.debug["dbtimer"]+=time.time()-t
		if D: env.dbg("'query' returned %s",result)
		if result:
			if D: env.dbg("Creating list of ordered dicts.")
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
					#if D and first: env.info("'%s' appended as node",col)
					nodes.append((fields[i],None,[row[i]]))
				first=False
				ret.append(Object(nodes))
			if len(ret) is 1:
				#row
				return ret[0]
				#if len(ret[2]) is 1:
				#	#value
				#	return Object(ret[2][0][2][0])
			else:
				return List(ret) #("list",{},ret)
		else:
			return Object()
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
