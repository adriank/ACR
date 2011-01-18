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

class Default(Component):
	def generate(self, env,config):
		D=env.doDebug
		if D: env.debug("Starting default component generation with %s"%config)
		o=Object()
		if config.has_key("output") and config["output"]:
			o.set(replaceVars(env, config["string"],escape))
		else:
			o.set(replaceVars(env, config["string"]))
			o._doFn=False
		if D: env.debug("Returning %s"%o._value)
		return o

	def parseAction(self,config):
		s=[]
		for elem in config["content"]:
			if type(elem) is tuple:
				s.append(tree2xml(elem,True))
			elif type(elem) is str:
				s.append(elem)
		return {"string":prepareVars("".join(s)), "output":config.get("output",None)}

def getObject(config):
	return Default(config)
