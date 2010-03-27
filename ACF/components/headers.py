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
from ACF.components import Component
from ACF.errors import *
#from ACF.db import pgsql
from ACF.utils import replaceVars,HTTP
import logging

log=logging.getLogger('ACF.component.headers')

class Headers(Component):
	def generate(self,env,config):
		action=config[0].split(":").pop().lower()
		if action=="redirect":
			log.info("Requested redirect to <a href=\"%s\">%s</a>",replaceVars(env,config[1]["location"]))
			env.doRedirect=True
			env.outputHeaders.append(("Location",replaceVars(env,config[1]["location"])))
		elif action=="cookie":
			if a[1]["action"].lower()=="set":
				d={"name":str(replaceVars(a[1]["name"])), "value":str(replaceVars(config[1]["value"]))}
				if a[1].has_key("path"):
					d["path"]=str(replaceVars(a[1]["path"]))
				HTTP.setCookie(d)
		return None

	#def parseAction(self,config):
	#	print "dupa"
	#	print config
	#	return {
	#		"action":config[0],
	#
	#	}

def getObject(config):
	return Headers(config)
