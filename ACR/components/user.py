#!/usr/bin/env python
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

from ACR.components import *
from ACR.utils import replaceVars,generateID
from ACR import globals
from ACR.errors import Error
from ACR.utils.hashcompat import md5_constructor
from ACR.session.file import FileSession

class User(Component):
	def login(self,acenv,conf):
		D=acenv.doDebug
		ret=Object()
		email=replaceVars(acenv,conf["email"])
		password=replaceVars(acenv,conf["password"])
		sql="select password,id,role from %s.users where id=(select _user from %s.emails where email='%s')"%(globals.dbschema,globals.dbschema,email)
		try:
			result=acenv.app.getDBConn().query(sql)
			result=dict(zip(result["fields"], result["rows"][0]))
		except IndexError:
			if D: acenv.error("Account not found")
			ret.status="error"
			ret.error="AccountNotFound"
			return ret
		if result['password']==md5_constructor(password).hexdigest():
			if D: acenv.info("Password is correct")
			if not acenv.sessionStorage:
				acenv.sessionStorage=FileSession(acenv)
			if D: acenv.info("Setting ID=%s, email=%s and role=%s to session",result['id'],email,result['role'])
			acenv.sessionStorage["ID"]=result['id']
			acenv.sessionStorage["email"]=email
			acenv.sessionStorage["role"]=result['role']
			#is it necessary?
			acenv.sessionStorage["loggedIn"]=True
			#acenv.session["fake"]=False
			return ret
		else:
			if D: acenv.error("Password is not correct")
			ret.status="error"
			ret.error="WrongPassword"
			return ret

	def logout(self,acenv,conf):
		try:
			acenv.sessionStorage.delete()
		except:
			pass
		return Object()

	def register(self,acenv,conf):
		email=replaceVars(acenv,conf["email"])
		password=replaceVars(acenv,conf["password"])
		sql="select exists(select * from %s.emails where email='%s')"%(globals.dbschema,email)
		key=md5_constructor(password).hexdigest()
		#returns False if email is not registered yet
		if acenv.app.getDBConn().query(sql)["rows"][0][0]:
			o=Object()
			o.error="EmailAdressAllreadySubscribed"
			return o
		id="SELECT currval('%s.users_id_seq')"%(globals.dbschema)
		sql="""INSERT into %s.users
			(password)
		VALUES
			('%s');
		INSERT into %s.emails
			(email,_user,approval_key)
		VALUES
			('%s', (%s), '%s')"""%(globals.dbschema,key,globals.dbschema,email,id,generateID())
		result=acenv.app.getDBConn().query(sql)
		acenv.requestStorage["approval_key"]=key
		return Object()

	def generate(self,acenv,conf):
		return self.__getattribute__(conf["command"].split(":").pop())(acenv,conf)

	def parseAction(self,config):
		if config["command"] not in ["register","logout","login"]:
			raise Error("Bad command %s",config["command"])
		if config["command"] in ["register","login"] and not ("email" in config["params"].keys() or  "password" in config["params"].keys()):
			raise Error("Email or password is not set in %s action."%(config["command"]))
		ret=config["params"].copy()
		ret["command"]=config["command"]
		return ret

def getObject(config):
	return User(config)