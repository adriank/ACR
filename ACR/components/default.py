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

from ACR.utils import replaceVars,prepareVars
from ACR.components import *
from ACR.utils.xmlextras import tree2xml
from xml.sax.saxutils import escape,unescape

EXEC_CMD=("exec","execute","expr")

class Default(Component):
	def generate(self, env, config):
		if config.get("command"):
			return self.execute(env,config)
		D=env.doDebug
		if D: env.debug("START default:generation with %s", config)
		ret=replaceVars(env, config["string"],str)
		if D: env.debug("END default component generation with: '%s...'", ret)
		return ret

	def execute(self, acenv, conf):
		D=acenv.doDebug
		if D: acenv.debug("START default:Interpreter with: '%s'", conf["expr"].tree)
		try:
			ret=conf["expr"].execute(acenv)
			if D: acenv.debug("END default:Interpreter with: '%s'", ret)
			return ret
		except Exception,e:
			if D: acenv.error("Execution failed with error: %s", str(e))
			return {
				"@status":"error",
				"@error":"ExecutionFailedError",
				"@message":str(e)
			}

	def parseAction(self,config):
		cmd=config.get("command")
		if cmd in EXEC_CMD:
			return {
				"expr":make_tree("".join(config["content"]).strip()),
				"command":"exec"
			}
		s=[]
		for elem in config["content"]:
			if type(elem) is tuple:
				s.append(tree2xml(elem,True))
			elif type(elem) is str:
				s.append(elem)
		return {
			"string":prepareVars("".join(s).strip()),
			"output":config.get("output",None)
		}

def getObject(config):
	return Default(config)
