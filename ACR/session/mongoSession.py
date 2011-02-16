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
import time

class MongoSession(Session):
	def __init__(self, acenv, ID=None):
		self.env=acenv
		D=acenv.doDebug
		if D: acenv.info("START MongoSession.__init__ Created Session object with id=%s",id)
		#TODO check if dir exists and raise error when not
		self.sessCollection=acenv.app.storage[acenv.app.DB_NAME].session
		super(MongoSession, self).__init__(acenv,ID)

	def save(self):
		self.env.info("Saving session")
		if not self.modified:
			self.env.info("Session is not modified")
			return
		self.env.info("Session is modified")
		if self.delCookie:
			self.deleteCookie()
		self.data["_id"]=self.ID
		self["last_login"]=time.time()
		self.sessCollection.save(self.data)

	def load(self):
		self.data=list(self.sessCollection.find({"_id":self.ID}))[0]

	def delete(self):
		self.sessCollection.remove({"_id":self.ID})
		self.delCookie=True

	def exists(self,id):
		return False
