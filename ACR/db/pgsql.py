#!/usr/bin/python
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

import psycopg2 as dbapi
from ACR import acconfig
from ACR.errors import Error
from ACR.utils.xmlextras import escapeQuotes

class handler(object):
	def __init__(self,conf):
		#if D: log.debug("Initialized with conf=%s",conf)
		host=""
		if conf.get("host"):
			host=conf["host"]#+":"+(conf.get("port","") or "5432")
		#if D: log.debug("Host is %s (None means socket)",host)
		self.conn=dbapi.connect("dbname='"+conf["defaultdb"]+"' host='"+host+"' user='"+conf["user"]+"' password='"+conf["password"]+"'")
		self.conn.set_isolation_level(0)
		#if D: log.info("Successfuly connected to PostgreSQL.")
		#q="SET CLIENT_ENCODING TO '';SET search_path TO "+acconfig.dbschema+", public"
		#if conf.has_key("schema"):
		#	q+=", "+conf["schema"]
		#TODO lazy query - should be executed with first query
		#if D: log.warning("Internal database query. Change debug level to 'debug' to see details.")
		#try:
		#	self.query(q)
		#except:
		#	pass

	def query(self,sql):
		#if D: log.debug("Executing with sql='%s' and dictionary=%s",sql,dictionary)
		#if acconfig.config.has_key("debug") and acconfig.config["debug"]:
		#	import time
		#	t=time.time()
		#return None
		cursor=self.conn.cursor()
		try:
			cursor.execute(sql)
			#self.conn.commit()
		except Exception ,e:
			#if D: log.error("SQLError %s",str(e))
			raise Error("SQLError",escapeQuotes(str(e))+": "+sql)
		#if D: log.info("Query returned rows (there was SELECT)")
		#this is most most memory efficient structure but needs to be replaced with yield by merging it with pygresql
		try:
			d={
				"rows":cursor.fetchall(),
				"fields":map(lambda x: x[0], cursor.description)
			}
			cursor.close()
			return d
		except:
			cursor.close()
			return None
