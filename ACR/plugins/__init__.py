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

from ACR.utils import conditionchecker,replaceVars
from ACR import acconfig
from ACR.errors import *
import logging
import sys

log = logging.getLogger('ACR.plugin')

#dict of component modules
PLUGIN_CACHE={}

def get(name):
	"""
		Returns component of given name. Manages components cache.
	"""
	module=PLUGIN_CACHE.get(name,None)
	if module:
		return module
	path="ACR.plugins."+name
	try:
		__import__(path)
	except ImportError,e:
		raise e
		raise Error("ComponentNotFound",str(e))
	m=sys.modules[path]
	PLUGIN_CACHE[name]=m
	return m

#abstract class
class Plugin(object):
	def __init__(self, config):
		self.config=config

	def getRootElement(self):
		raise AbstractClass()

def parseConfig(fragment):
	"""fragment is set of nodes"""
