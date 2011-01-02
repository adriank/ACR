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

from ACR.components import *
from ACR.utils import replaceVars
from ACR.utils.xmlextras import tree2xml
from ACR import acconfig
from ACR.errors import Error
from ACR.utils import json

class DataGenerator(Component):
	def list(self,acenv,conf):
		return List(replaceVars(acenv, conf["content"]))

	def generate(self,acenv,conf):
		return self.__getattribute__(conf["command"].split(":").pop())(acenv,conf)

	def parseAction(self,config):
		ret=config["params"].copy()
		ret["command"]=config["command"]
		if ret.has_key("input") and ret["input"]=="json":
			ret["content"]=json.loads("".join(config["content"]))
		else:
			r=[]
			for i in config["content"]:
				if type(i) is not str:
					r.append(tree2xml(i))
			ret["content"]="".join(r)
		return ret

def getObject(config):
	return DataGenerator(config)
