#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Asyncode Runtime - XML framework allowing developing internet
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

from ACR.utils.interpreter import execute,make_tree
from ACR.components import Component
from ACR.utils.generations import Object

class Interpreter(Component):
	def generate(self, acenv, conf):
		D=acenv.doDebug
		if D: acenv.debug("Executing expression '%s'", (conf["expression"]))
		try:
			o=Object(execute(conf["expression"]))
		except:
			if D: acenv.warning("Execution failed with error: %s", (str(e)))
			o=Object()
			o.status="error"
			o.error="ExecutionFailed"
		return o

	def parseAction(self, config):
		if config["command"] not in ["execute"]:
			raise Exception("Bad command %s" % config["command"])
		return {
			"expression":make_tree("".join(config["content"]).strip().split("\n"))
			#"command":config["command"]
		}

def getObject(config):
	return Interpreter(config)
