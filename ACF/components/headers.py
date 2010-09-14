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
from ACF.components import *
from ACF.errors import *
#from ACF.db import pgsql
from ACF.utils import replaceVars,HTTP
import logging

log=logging.getLogger('ACF.component.headers')

class Headers(Component):
	def setcookie(self,env,config):
		if a[1]["action"].lower()=="set":
			d={"name":replaceVars(env,a["name"]), "value":replaceVars(env,config["value"])}
			if a[1].has_key("path"):
				d["path"]=str(replaceVars(env,a[1]["path"]))
			HTTP.setCookie(env,d)

	def redirect(self,env,config):
		log.info("Requested redirect to <a href=\"%s\">%s</a>",replaceVars(env,config["location"]))
		env.doRedirect=True
		env.outputHeaders.append(("Location",replaceVars(env,config["location"])))
		return Object() #("object",{"status":"ok"},None)

	def generate(self,env,config):
		return self.__getattribute__(config["command"].split(":").pop())(env,config["params"])

def getObject(config):
	return Headers(config)
