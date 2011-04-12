#!/usr/bin/python
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

# highly modified Django code, relicensed under GPL

from ACR.session import Session
from ACR.errors import Error
import pymongo
from ACR.utils import now
"""
	Session is stored in Mongo as object where:
	-
"""

class MongoSession(Session):
	def __init__(self, acenv, ID=None):
		self.D=acenv.doDebug
		self.P=acenv.doProfiling
		if self.D: acenv.info("START MongoSession.__init__ Created Session object with id=%s",ID)
		#TODO check if dir exists and raise error when not
		self.sessCollection=acenv.app.storage.session
		super(MongoSession, self).__init__(acenv,ID)

	def save(self):
		if self.D: self.env.info("Saving session")
		if self.delCookie:
			self.deleteCookie()
			return
		if not self.data.has_key("_id"):
			self.data["_id"]=self.sessID
		self["last_login"]=now()
		if self.P: t=time.time()
		self.sessCollection.save(self.data)
		if self.P:
			self.env.profiler["dbtimer"]+=time.time()-t
			self.env.profiler["dbcounter"]+=1

	def load(self):
		if self.P: t=time.time()
		self.data=list(self.sessCollection.find({"_id":self.sessID}))[0]
		if self.P:
			self.env.profiler["dbtimer"]+=time.time()-t
			self.env.profiler["dbcounter"]+=1
		self.sessID=str(self.data.pop("_id"))
		if self.D: self.env.debug("Loaded session: %s",self.data)

	def delete(self):
		if self.P: t=time.time()
		self.sessCollection.remove({"_id":self.sessID})
		if self.P:
			acenv.profiler["dbtimer"]+=time.time()-t
			acenv.profiler["dbcounter"]+=1
		self.delCookie=True

	def exists(self,id):
		return False
