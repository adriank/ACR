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

# This file takes one BLSL file and outputs its JSON representation

from ACR.utils.xmlextras import *
from ACR import acconfig
from ACR import components
from ACR.errors import *
from ACR.utils import getStorage,prepareVars,typesMap,str2obj,iterators
from ACR.utils.interpreter import makeTree,Tree
import os,re

NODE="node"
SET="set"
UNSET="unset"
PUSH="push"
INSERT="insert"

COMMAND="command"
INHERITS="inherits"
IMPORT="import"

WRITE_COMMANDS=[UNSET,SET,PUSH,INSERT]
ACTIONS=WRITE_COMMANDS+[NODE]

def parsePosts(nodes):
	if not nodes:
		return (None,None)
	ret={}
	postCount=0
	for i in nodes:
		attrs=i[1]
		typ=typesMap.get(attrs.get("type","default").lower())()
		if attrs.has_key("default"):
			typ.setDefault(makeTree(attrs["default"]))
		else:
			postCount+=1
		ret[attrs["name"]]=typ
	return (ret,postCount)

def parseInputs(nodes):
	if not nodes:
		return None
	ret=[]
	postCount=0
	for i in nodes:
		attrs=i[1]
		try:
			typ=typesMap.get(attrs.get("type","default").lower())()
		except TypeError:
			raise Error("WrongInputTypeName","Input type '%s' is not supported."%attrs.get("type","default"))
		if attrs.has_key("default"):
			typ.setDefault(makeTree(attrs["default"]))
		ret.append({
			"name":attrs["name"],
			"type":typ
		})
	return ret
