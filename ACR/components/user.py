#!/usr/bin/env python
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

from ACR.components import *
from ACR.utils import replaceVars,generateID
from ACR.utils.interpreter import makeTree
from ACR import acconfig
from ACR.errors import Error
from ACR.utils.hashcompat import md5_constructor
from ACR.session.mongoSession import MongoSession
import re

"""
	Users are stored in the Mongo:
	- email is required for now and acts as unique key until other login types will be implemented (uniquenes is handled here because Mongo does not support null - null is a value so only one object without email can exist),
	- password is md5 of password; currently passing md5 string directly from UA is not supported
	- role is for handling simple role-based privilege system,
	- privileges is a list of names of privileges granted to user,
	- approval_key is key that user need to authorize his e-mail address (anty-spamm strategy and ensuring that user owns address)

--- Possible extensions ---

	- handling md5 passwords directly from UA instead of hashing it here,
	- login via OpenID
	- OAuth
"""

class User(Component):
	#defaults
	ROLE="user"
	APPROVED=False
	MAIN=False
	EMAIL_RE=re.compile("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$")


	def login(self,acenv,conf):
		D=acenv.doDebug
		email=replaceVars(acenv,conf["email"]).lower()
		usersColl=acenv.app.storage.users
		try:
			user=list(usersColl.find({
				"email":email,
				'$or': [
					{'suspended': {'$exists': False}},
					{'suspended': False}
				]
			}))[0]
		except IndexError:
			if D: acenv.error("Account not found")
			return {
				"@status":"error",
				"@error":"AccountNotFound"
			}
		password=replaceVars(acenv,conf["password"])
		if user['password']==md5_constructor(password).hexdigest():
			if D: acenv.info("Password is correct")
			if not acenv.sessionStorage:
				acenv.sessionStorage=MongoSession(acenv)
			if D: acenv.info("Setting session as:\n	%s",user)
			user["ID"]=str(user.pop("_id"))
			user["loggedIn"]=True
			acenv.sessionStorage.data=user
			#print "login sess data ",acenv.sessionStorage.data
			return {"@status":"ok"}
		else:
			if D: acenv.error("Password is not correct")
			return {
				"@status":"error",
				"@error":"WrongPassword"
			}

	def logout(self,acenv,conf):
		try:
			acenv.sessionStorage.delete()
		except:
			pass
		return {"@status":"ok"}

	def register(self,acenv,conf):
		usersColl=acenv.app.storage.users
		email=replaceVars(acenv,conf["email"]).lower()
		if not (len(email)>5 and self.EMAIL_RE.match(email)):
			return {
				"@status":"error",
				"@error":"NotValidEmailAddress",
				"@message":"Suplied value is not a valid e-mail address"
			}
		if list(usersColl.find({"email":email})):
			return {
				"@status":"error",
				"@error":"EmailAdressAllreadySubscribed",
				"@message":"User already exists in the system"
			}
		key=generateID()
		d={
			"email":email,
			"password":md5_constructor(replaceVars(acenv,conf["password"])).hexdigest(),
			"role":replaceVars(acenv,conf.get("role",self.ROLE)),
			"approvalKey":key,
			"privileges":[]
		}
		if conf.has_key("data"):
			d.update(conf["data"].execute(acenv))
		id=usersColl.save(d,safe=True)
		return {
			"@status":"ok",
			"@id":id,
			"@approvalKey":key
		}

	def generate(self,acenv,conf):
		return self.__getattribute__(conf["command"].split(":").pop())(acenv,conf)

	def parseAction(self,config):
		if config["command"] not in ["register","logout","login"]:
			raise Error("Bad command %s",config["command"])
		if config["command"] in ["register","login"] and not ("email" in config["params"].keys() or  "password" in config["params"].keys()):
			raise Error("Email or password is not set in %s action."%(config["command"]))
		ret=config["params"].copy()
		if ret.has_key("data"):
			ret["data"]=makeTree(ret["data"])
		ret["command"]=config["command"]
		return ret

def getObject(config):
	return User(config)
