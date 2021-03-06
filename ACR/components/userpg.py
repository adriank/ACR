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
from ACR import acconfig
from ACR.errors import Error
from ACR.utils.hashcompat import md5_constructor
from ACR.session.mongoSession import MongoSession

class User(Component):
	#defaults
	ROLE="user"
	APPROVED=False
	MAIN=False

	def login(self,acenv,conf):
		D=acenv.doDebug
		email=replaceVars(acenv,conf["email"])
		password=replaceVars(acenv,conf["password"])
		sql="select password,id,role from %s.users where id=(select _user from %s.emails where email='%s')"%(acconfig.dbschema,acconfig.dbschema,email)
		try:
			result=acenv.app.getDBConn().query(sql)
			result=dict(zip(result["fields"], result["rows"][0]))
		except IndexError:
			if D: acenv.error("Account not found")
			return {
				"@status":"error",
				"@error":"AccountNotFound"
			}
		if result['password']==md5_constructor(password).hexdigest():
			if D: acenv.info("Password is correct")
			if not acenv.sessionStorage:
				acenv.sessionStorage=MongoSession(acenv)
			if D: acenv.info("Setting ID=%s, email=%s and role=%s to session",result['id'],email,result['role'])
			acenv.sessionStorage["ID"]=result['id']
			acenv.sessionStorage["email"]=email
			acenv.sessionStorage["role"]=result['role']
			#is it necessary?
			acenv.sessionStorage["loggedIn"]=True
			#acenv.session["fake"]=False
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

	#TODO test and debug!
	def register(self,acenv,conf):
		email=replaceVars(acenv,conf["email"])
		password=replaceVars(acenv,conf["password"])
		role=replaceVars(acenv,conf.get("role",self.ROLE))
		sql="select exists(select * from %s.emails where email='%s')"%(acconfig.dbschema,email)
		passwd=md5_constructor(password).hexdigest()
		key=generateID()
		#returns False if email is not registered yet
		if acenv.app.getDBConn().query(sql)["rows"][0][0]:
			return {
				"error":"EmailAdressAllreadySubscribed"
			}
		#XXX implement psycopg escaping!!!
		id="SELECT currval('%s.users_id_seq')"%(acconfig.dbschema)
		sql="""INSERT into %s.users
			(password,role)
		VALUES
			('%s', '%s');
		INSERT into %s.emails
			(email,_user,approval_key,approved,main)
		VALUES
			('%s', (%s), '%s', %s, %s)"""%(
			acconfig.dbschema,
			passwd,
			role,
			acconfig.dbschema,
			email,
			id,
			key,
			conf.get("approved",self.APPROVED),
			conf.get("approved",self.MAIN)
		)
		result=acenv.app.getDBConn().query(sql)
		acenv.requestStorage["approval_key"]=key
		return {"status":"ok"}

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
