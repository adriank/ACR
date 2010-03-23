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


from ACF import globals
from ACF.utils.hashcompat import md5_constructor
from ACF.components.base import Component
from ACF.utils import conditionchecker,replaceVars
from ACF.errors import *
from ACF.session.file import FileSession
from ACF.utils.xmlextras import dom2tree
import logging
log = logging.getLogger('ACF.component.userLogin')

class UserLogin(Component):
	def __init__(self,config):
		log.info("Created instance with config=%s",config)
		self.db=globals.getDB()
		self.config=config
		self.actions=self.config["actions"]
		log.debug("Actions is %s",self.actions)

	def handle(self,data):
		log.debug("Executing with data=%s",data)
		session=globals.session
		action=self.actions[0]
		if action[0]=="logout":
			log.info("Log out")
			session.delete()
			return
		email=replaceVars(action[1]["email"],data)
		password=replaceVars(action[1]["password"],data)
		sql="select password,id,role from "+globals.dbschema+".users where id=(select _user from "+globals.dbschema+".emails where email='"+email+"')"
		try:
			result=self.db.rawQuery(sql)[0]
		except IndexError:
			log.error("Account not found")
			raise Error("accountNotFound")
		if result['password']==md5_constructor(password).hexdigest():
			log.info("Password is correct")
			if session is None:
				session=FileSession()
			log.info("Setting ID=%s, email=%s and role=%s to session",result['id'],email,result['role'])
			session["ID"]=result['id']
			session["email"]=email
			session["role"]=result['role']
			session["loggedIn"]=True
			session["fake"]=False
			globals.session=session
			log.debug("Session is %s",globals.session.data)
		else:
			log.error("Wrong password")
			raise Error("WrongPassword")
		return "ok"

def parseConfig(root):
	r=dom2tree(root)[2]
	conditions=[]
	actions=[]
	for elem in r:
		if elem[0].lower()=="conditions":
			for e in elem[2]:
				conditions.append(conditionchecker.parseConfig(e))
		else:
			actions.append(elem)
	return {
		"conditions":conditions,
		"actions":actions
	}


def getObject(config):
	return UserLogin(config)
