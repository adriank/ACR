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
from ACF.utils import mail,replaceVars
from ACF.components import *
#from ACF.utils.xmlextras import dom2tree
from ACF.errors import *
import os
import re

class Email(Component):
	def generate(self,acenv,conf):
		content=conf["content"]
		headers={}
		params=conf["params"]
		for h in params:
			headers[h]=replaceVars(acenv,params[h])
			typ=type(params[h])
			if typ is list:
				headers[h]=map(lambda x: replaceVars(acenv,x),headers[h])
		mail.send(headers,replaceVars(acenv,content))
		return Object()

	def parseAction(self,conf):
		params={}
		for h in conf["params"]:
			params[h.capitalize()]=conf["params"][h]
		conf["params"]=params
		try:
			conf["params"]["From"]
		except KeyError:
			raise Error("FromAdressNotSpecified", "'from' should be specified")
		try:
			conf["params"]["To"]
		except KeyError:
			raise Error("ToAdressNotSpecified", "'to' should be specified")
		try:
			conf["params"]["Subject"]
		except KeyError:
			raise Error("SubjectNotSpecified", "'subject' should be specified")
		conf['content']="".join(conf['content'])
		return conf

def getObject(config):
	return Email(config)
