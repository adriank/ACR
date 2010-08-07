#!/usr/bin/env python
import sys,time,random,base64
from datetime import datetime, timedelta
from ACF.errors import *
from ACF.utils.hashcompat import md5_constructor
import re
from ACF import globals

if hasattr(random, 'SystemRandom'):
	randrange=random.SystemRandom().randrange
else:
	randrange=random.randrange

PREFIX_DELIMITER="::"
RE_PATH=re.compile("{\$([^}]+)}")
#log=logging.getLogger('ACF.util')
#D=logging.doLog
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

#returns value from dict hierarchy based on "a.b.c" paths
def objectPath(obj,path):
	t=path.split(".")
	i=None
	try:
		i=t[0]
		ret=obj[i]
		for i in t:
			_type=type(ret)
			if _type is dict:
					ret=ret[i]
	except (AttributeError, KeyError, TypeError):
		if D: log.warning("%s",e)
		return False
	return ret

def evaluate(v):
	t=v.split(".")
	if D: log.debug("Storage name is %s",t[0])
	ret=getStorage(t[0])
	if D: log.debug("Storage content is %s",ret)
	t.pop(0)
	try:
		for i in t:
			if ret.has_key(i):
				ret=ret[i]
	except (AttributeError,KeyError),e:
		if D: log.warning("%s",e)
		return False
	return ret

def replaceVars(env,s):
	def parse(m):
		p=m.group(0)[2:-1]
		storageName=""
		try:
			storageName,path=p.split(PREFIX_DELIMITER)
			storage=getStorage(env,storageName)
		except ValueError:
			storage=getStorage(env,"rs")
			path=p
		ret=objectPath(storage,path)
		if type(ret) is list:
			return m.group(0)
		if not ret:
			raise Exception((storageName or "rs")+" storage does not have "+path+" property")
		return str(ret)

	#can be even faster "%(vals)" and "%{vals}" are 3x faster
	if type(s) is not str:
		raise Exception("Not string, but "+str(s))
	return RE_PATH.sub(parse, s)

def generateID(secret=None):
	if secret is None:
		secret=globals.SECRET_KEY
	key = md5_constructor("%s%s%s%s" % (randrange(0, 184467440737096L), 144, time.time(), secret)).hexdigest()
	return key
