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
from ACR.utils import mail,replaceVars
from ACR.components import *
#from ACR.utils.xmlextras import dom2tree
from ACR.errors import *
import os
import re
from ACR.utils import dicttree,PREFIX_DELIMITER,getStorage,RE_PATH
import subprocess

class Exec(Component):
	def generate(self,acenv,conf):
		command=conf["params"]["exec"]
		content=replaceVars(acenv,content)
		start=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		start.stdin.write(conf["content"])
		start.wait()
		start.stdin.close()
		return start.stdout.read()

	def parseAction(self,conf):
		try:
			conf["params"]["exec"]
		except KeyError:
			raise Error("execNotSpecified", "'exec' should be specified")
		conf['content']="".join(conf['content'])
		return conf

def getObject(config):
	return Exec(config)
