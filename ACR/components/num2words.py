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

from ACR.components import *
from ACR.errors import *
from ACR.utils import replaceVars, num2words as n2w, prepareVars

class Num2Words(Component):
	def num2words(self,env,config):
		print config
		return n2w.liczba_slownie(config["number"])

	def generate(self,env,config):
		return self.__getattribute__(config["command"].split(":").pop())(env,config)

	def parseAction(self,config):
		s=[]
		for elem in config["content"]:
			if type(elem) is str:
				s.append(elem)
		return {
			"command":config["command"],
			"number":prepareVars("".join(s).strip()),
		}

def getObject(config):
	return Num2Words(config)
