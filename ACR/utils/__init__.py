#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,time,random,base64,re
from datetime import datetime, timedelta
from ACR.errors import *
from ACR.utils.hashcompat import md5_constructor
from ACR.utils.xmlextras import escapeQuotes
from ACR.utils import dicttree
from ACR.utils.generations import Object,List
from ACR import globals

if hasattr(random, 'SystemRandom'):
	randrange=random.SystemRandom().randrange
else:
	randrange=random.randrange

PREFIX_DELIMITER="::"
RE_PATH=re.compile("{\$([^}]+)}") # {$ foobar}
RE_PATH_split=re.compile("{\$[^}]+}") # {$ foobar}
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

def replaceVars_new(env,l,fn=None):
	if type(l) is str:
		return l
	#print "replaceVars_new"
	#print l
	ret=[]
	for i in l:
		if type(i) is tuple:
			storage=getStorage(env,i[0])
			v=dicttree.get(storage,i[1])
			doFN=True
			if type(v) is Object:
				try:
					doFN=v._doFn
				except:
					pass
				v=v._value
			if type(v) is not List:
				v=str(v)
				if fn and doFN:
					v=fn(v)
			ret.append(v)
		else:
			ret.append(i)
	if len(ret) is 1:
		return ret[0]
	try:
		return "".join(ret)
	except TypeError,e:
		return ret

def replaceVars(env,s,data=None,escape=False):
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
		if escape:
			ret=escapeQuotes(str(ret))
		if ret is None:
			return "null"
		if type(ret) not in [str,Object]:
			return m.group(0)
		#keep is None; "" is proper value
		#if ret is None:
		#	raise Error("NoVariable",(storageName or "rs")+" storage does not have "+".".join(path)+" property")
		return str(ret)

	#can be even faster ""%(vals) and ""%{vals} are 3x faster
	if type(s) is not str:
		raise Error("NotString","Not string, but "+str(s))
	return RE_PATH.sub(parse, s)

def prepareVars(s):
	splitted=RE_PATH_split.split(s)
	vars=RE_PATH.findall(s)
	ret=[]
	try:
		while True:
			ret.append(splitted.pop(0))
			var=vars.pop(0)
			try:
				storageName,path=var.split(PREFIX_DELIMITER)
			except ValueError:
				storageName="rs"
				path=var
			path=path.split(".")
			ret.append((storageName,path))
	except:
		pass
	if ret[0]=="":
		ret.pop(0)
	if ret and ret[-1]=="":
		ret.pop()
	if len(ret) is 1 and type(ret[0]) is str:
		ret=ret[0]
	return ret

def generateID(secret=None):
	if secret is None:
		secret=globals.SECRET_KEY
	key=md5_constructor("%s%s%s%s" % (randrange(0, 184467440737096L), 144, time.time(), secret)).hexdigest()
	return key

from ACR.utils import types
typesMap={
	"default":types.Type,
	"text":types.Text,
	"xml":types.Type,
	"email":types.Email,
	"number":types.Number,
	"empty":types.Empty,
	"nonempty":types.NonEmpty,
	"hexcolor":types.HEXColor
}
