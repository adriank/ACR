#!/usr/bin/env python
# -*- coding: utf-8 -*-

# AsynCode Framework - XML framework allowing developing internet
# applications without using programming languages.
# Copyright (C) 2008-2010  Adrian Kalbarczyk, Marcin Radecki

# This program is free software: you can redistribute it and/or modify
# it under the terms of the version 3 of GNU General Public License as published by
# the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ACF.utils.interpreter import execute,make_tree
from ACF.utils import getStorage
from ACF.components import Component
from ACF.utils.generations import Object

class Interpreter(Component):
	def generate(self,acenv, config):
		return self.__getattribute__(config["command"])(acenv,config)
	
	def parseAction(self, config):
		if config["command"] not in ["checkCondition"]:
			raise Exception("Bad command %s" % config["command"])
		if (config["command"] == "checkCondition") and not ("name" in config["params"].keys() and "condition" in config["params"].keys()):
			raise Exception("Missing command '%s' parameters" % config["command"])
		ret=config["params"].copy()
		ret["command"]=config["command"]
		return ret
	
	def checkCondition(self, acenv, conf):
		"""
			Check condition via internal condition languge interprater
			and writes returned value to a variable.
			Parameters:
				name: returned value will be assigned to a variable called 'name', required
				condition: a condition to be checked, required
				storage: which storage the variable belongs to, non required, default is request storage
		"""
		D=acenv.doDebug
		if D: acenv.debug("Executing command interpreter.checkCondition(%s, %s)" % (conf["name"], conf["condition"]))
		if conf.has_key("storage"):
			storage=getStorage(acenv, conf["storage"])
		else:
			storage=acenv.requestStorage
		try:
			storage[conf["name"]]=execute(acenv, make_tree(conf["condition"]))
			if D: acenv.debug("Condition execution succesful, returned %s" % storage[conf["name"]])
			return Object()
		except Exception, e:
			if D: acenv.info("Condition %s execution failed with error: %s" % (conf["name"], str(e)))
			o=Object()
			o.status="error"
			o.error="ExecutionFailed"
			return o
			
def getObject(config):
	return Interpreter(config)