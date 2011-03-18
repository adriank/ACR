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

from ACR.utils.interpreter import make_tree
from ACR.components import Component

class Interpreter(Component):
	def generate(self, acenv, conf):
		D=acenv.doDebug
		if D: acenv.debug("START Interpreter with: '%s'", conf["expression"].tree)
		try:
			if D: acenv.debug("END Interpreter with: '%s'", o._value)
			return conf["expression"].execute(acenv)
		except Exception,e:
			if D: acenv.error("Execution failed with error: %s", str(e))
			return {
				"status":"error",
				"error":"ExecutionFailed"
			}

	def parseAction(self, config):
		if config["command"] not in ["execute","exec"]:
			raise Exception("Bad command %s" % config["command"])
		return {
			"expression":make_tree("".join(config["content"]).strip())
			#"command":config["command"]
		}

def getObject(config):
	return Interpreter(config)
