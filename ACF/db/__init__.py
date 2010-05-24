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
from ACF.errors import *
import sys
import logging
import pg

log=logging.getLogger('ACF.db')

DRIVER_CACHE={}
CONFIG_CACHE={}

def get(conf,reload=False):
	"""
		Returns connection object of given config. Manages connection cache.
		config's "appName" value secures driver from being used by other apps
		conf can contain only the "name" if we are sure the connection exists.
		WARNING! connections can be broken by external events such as dbms
		restart! CONFIG_CACHE is for reseting connections.
	"""
	log.debug("Executing with conf=%s and reload=%s",conf,reload)
	uid=str(conf)
	if not reload:
		object=DRIVER_CACHE.get(uid,None)
		if object:
			#print "DB from cache"
			log.debug("Returning from cache")
			return object
	else:
		conf=CONFIG_CACHE[uid]
	path="ACF.db."+conf["dbms"]
	try:
		__import__(path)
	except ImportError,e:
		raise Error("DBDriverNotFound",str(e))
	driver=sys.modules[path].handler(conf)
	DRIVER_CACHE[uid]=driver
	CONFIG_CACHE[uid]=conf
	if conf.get("default",False):
		DRIVER_CACHE[uid+"default"]=driver
		CONFIG_CACHE[uid+"default"]=conf
	#print "DB not from cache"
	return driver

def escapeString(s):
	log.debug("start with string='%s'",s)
	if type(s) in [str,unicode]:
		try:
			return pg.escape_string(s)
		except:
			log.warning("There is no escape_string in PyGreSQL. Please update backend.")
			return s
