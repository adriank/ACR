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

#######################
#  	  DEPRECATED      #
#######################

from ACR.utils.interpreter import makeTree
from ACR.components import Component

class Interpreter(Component):
	def generate(self, acenv, conf):
		D=acenv.doDebug
		if D: acenv.start("Interpreter with: '%s'", conf["expression"].tree)
		#try:
		ret=conf["expression"]
		if D: acenv.end("Interpreter with: '%s'", ret)
		return ret
		#except Exception,e:
		#	if D: acenv.error("Execution failed with error: %s", str(e))
		#	return {
		#		"@status":"error",
		#		"@error":"ExecutionFailed",
		#		"@message":str(e)
		#	}

	def parseAction(self, config):
		if config["command"] not in ["execute","exec"]:
			raise Exception("Bad command %s" % config["command"])
		return {
			"expression":makeTree("".join(config["content"]).strip())
			#"command":config["command"]
		}

def getObject(config):
	return Interpreter(config)
