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

from ACR import acconfig
from ACR.components import *
from ACR.utils.generations import *
from ACR.errors import *
from ACR.utils import replaceVars_new,HTTP

class Headers(Component):
	def setcookie(self,env,config):
		#if config[1]["action"].lower()=="set":
		d={"name":replaceVars_new(env,config["name"]), "value":replaceVars_new(env,config["value"])}
		if config.has_key("path"):
			d["path"]=replaceVars_new(env,config["path"])
		HTTP.setCookie(env,d)
		return Object()

	def redirect(self,env,config):
		if env.doDebug: env.info("Requested redirect to <a href=\"#\">%s</a>"%(replaceVars_new(env,config["location"])))
		env.doRedirect=True
		env.outputHeaders.append(("Location",replaceVars_new(env,config["location"])))
		return Object() #("object",{"status":"ok"},None)

	def generate(self,env,config):
		return self.__getattribute__(config["command"].split(":").pop())(env,config["params"])

def getObject(config):
	return Headers(config)
