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
from ACF.utils import mail,conditionchecker,replaceVars,generateID
from ACF.components.base import Component
from ACF.utils.hashcompat import md5_constructor
name="register user"

class userRegister(Component):
	def __init__(self,config):
		self.config=config
		self.db=globals.getDB()

	def handle(self,data):
		r=self.checkConditions(data)
		if r is not True:
				return [r]

		conf={
			"key":generateID("")
		}
		for i in ["email","password"]:
			conf[i]=replaceVars(self.config[i])

		result=self.db.rawQuery("select exists(select * from "+globals.dbschema+".emails where email='"+conf['email']+"') as result")[0]
		if result['result']=="t":
			return [("error", {"code":"EmailAdressAllreadySubscribed"},None)]

		sql=""
		id="SELECT currval('"+globals.dbschema+".users_id_seq')"
		if globals.config["session"]["fakeAccount"] and globals.session.has_key('ID'):
			id=str(globals.session['ID'])
			sql="update "+globals.dbschema+".users set password='"+md5_constructor(conf['password']).hexdigest()+"' where id="+id+";"
		else:
			sql="insert into "+globals.dbschema+""".users
			(password)
			VALUES
			('"""+md5_constructor(conf['password']).hexdigest()+"');"
		sql+="insert into "+globals.dbschema+""".emails
		(email,_user,approval_key)
		VALUES
		('"""+conf['email']+"', ("+id+"), '"+conf['key']+"')"
		self.db.rawQuery(sql)
		globals.requestStorage["verificationKey"]=conf['key']

		return "ok"

def parseConfig(root):
	d={
		"conditions":[],
		"verification":{}
	}
	for node in root.childNodes:
		if node.nodeType == node.ELEMENT_NODE:
			if node.nodeName.lower() == "condition":
				d['conditions'].append(conditionchecker.parseConfig(node))
			elif node.nodeName.lower() == "register":
				if node.attributes.has_key("email"):
					d['email']=node.attributes['email'].value
				if node.attributes.has_key("password"):
					d['password']=node.attributes['password'].value
			elif node.nodeName.lower() == "verificationmail":
				for i in node.attributes.keys():
					d['verification'][i]=node.attributes[i].value
				d['verification']['content']=node.firstChild.data
		d['errorString']="Wrong password suplied"
	if root.attributes.has_key('errorString'):
		d['errorString']=root.attributes['errorString'].value
	return d

def getObject(config):
	return userRegister(config)
