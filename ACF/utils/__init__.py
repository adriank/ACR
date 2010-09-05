#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,time,random,base64,re
from datetime import datetime, timedelta
from ACF.errors import *
from ACF.utils.hashcompat import md5_constructor
from ACF import globals
from ACF.utils.objecttree import *

if hasattr(random, 'SystemRandom'):
	randrange=random.SystemRandom().randrange
else:
	randrange=random.randrange

PREFIX_DELIMITER="::"
RE_PATH=re.compile("{\$([^}]+)}") # {$ foobar}
D=False

def getStorage(env,s):
	if D: log.debug("Executed with s=%s",s)
	s=s.lower()
	if s=="session" or s=="ss":
		if not env.sessionStorage:
			return False
		return env.sessionStorage
	#elif s=="request" or s=="rs":
	#	return
	elif s=="global" or s=="gs":
		return []
	return env.requestStorage

def replaceVars(env,s):
	def parse(m):
		p=m.group(0)[2:-1]
		storageName=""
		try:
			storageName,path=p.split(PREFIX_DELIMITER)
			storage=getStorage(env,storageName)
		except ValueError:
			storage=getStorage(env,"rs")
			path=p.split(".")
		ret=getObject(storage,path)
		if type(ret) is list:
			return m.group(0)
		if not ret:
			raise Exception((storageName or "rs")+" storage does not have "+path+" property")
		return str(ret)

	#can be even faster ""%(vals) and ""%{vals} are 3x faster
	if type(s) is not str:
		raise Exception("Not string, but "+str(s))
	return RE_PATH.sub(parse, s)

def generateID(secret=None):
	if secret is None:
		secret=globals.SECRET_KEY
	key = md5_constructor("%s%s%s%s" % (randrange(0, 184467440737096L), 144, time.time(), secret)).hexdigest()
	return key
