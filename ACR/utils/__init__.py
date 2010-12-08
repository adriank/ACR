#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,time,random,base64,re
from datetime import datetime, timedelta
from ACF.errors import *
from ACF.utils.hashcompat import md5_constructor
from ACF.utils import dicttree
from ACF.utils.generations import *
from ACF import globals

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
		return env.sessionStorage.data
	#elif s=="request" or s=="rs":
	#	return
	elif s=="global" or s=="gs":
		return {}
	return env.requestStorage

def replaceVars(env,s,data=None):
	def parse(m):
		p=m.group(0)[2:-1]
		storageName=""
		try:
			storageName,path=p.split(PREFIX_DELIMITER)
			storage=getStorage(env,storageName)
		except ValueError:
			storage=data or getStorage(env,"rs")
			path=p
		path=path.split(".")
		ret=dicttree.get(storage,path)
		if type(ret) not in [str,Object]:
			return m.group(0)
		#keep is None; "" is proper value
		if ret is None:
			raise Error("NoVariable",(storageName or "rs")+" storage does not have "+".".join(path)+" property")
		return str(ret)

	#can be even faster ""%(vals) and ""%{vals} are 3x faster
	if type(s) is not str:
		raise Error("NotString","Not string, but "+str(s))
	return RE_PATH.sub(parse, s)

def generateID(secret=None):
	if secret is None:
		secret=globals.SECRET_KEY
	key = md5_constructor("%s%s%s%s" % (randrange(0, 184467440737096L), 144, time.time(), secret)).hexdigest()
	return key
