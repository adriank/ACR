#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,time,random,base64,re
from datetime import datetime, timedelta
from ACR.errors import *
from ACR.utils.hashcompat import md5_constructor
from ACR.utils.xmlextras import escapeQuotes
from ACR.utils import dicttree
#from ACR.utils.interpreter import make_tree
from ACR import acconfig

if hasattr(random, 'SystemRandom'):
	randrange=random.SystemRandom().randrange
else:
	randrange=random.randrange

PREFIX_DELIMITER="::"
RE_PATH=re.compile("{\$([^}]+)}") # {$ foobar}
RE_PATH_split=re.compile("{\$[^}]+}") # {$ foobar}

def getStorage(env,s):
	D=env.doDebug
	if D:
		env.debug("START getStorage with s= '%s'",s)
	s=s.lower()
	if s=="session" or s=="ss":
		if not env.sessionStorage:
			if D: env.debug("END getStorage with: session do not exists")
			return False
		if D: env.debug("END getStorage with: session storage")
		return env.sessionStorage.data
	#elif s=="app" or s=="as":
	#	return
	#TODO cookie storage
	#elif s=="cookie" or s=="cs":
	#	return
	elif s=="global" or s=="gs":
		return {}
	if D: env.debug("END getStorage with: request storage")
	return env.requestStorage

def replaceVars(env,l,fn=None):
	"""
	l - output of prepareVars
	fn - function that will be executed on each string
	"""
	D=env.doDebug
	if D: env.debug("START replaceVars with: path='%s' and fn='%s'", l, fn)
	try:
		l.__iter__
	except:
		return l
	ret=[]
	for i in l:
		if type(i) is tuple:
			if D: env.debug("computing '%s'",i)
			storage=getStorage(env,i[0])
			v=dicttree.get(storage,i[1],acenv=env)
			doFN=True
			if D: env.debug("adding '%s' to the end of string",v)
			ret.append(v)
		else:
			if D: env.debug("adding '%s' to the end of string",i)
			ret.append(i)
	if len(ret) is 1:
		if D: env.debug("END replaceVars with: %s",ret[0])
		return ret[0]
	try:
		if D: env.debug("END replaceVars with: %s","".join(ret))
		return "".join(ret)
	except TypeError,e:
		if D: env.error("END replaceVars with TypeError: %s",ret)
		return ret

def prepareVars(s):
	if type(s) is not str:
		return s
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
		secret=acconfig.SECRET_KEY
	key=md5_constructor("%s%s%s%s" % (randrange(0, 184467440737096L), 144, time.time(), secret)).hexdigest()
	return key

from ACR.utils import types
typesMap={
	"default":types.Default,
	"text":types.Text,
	"xml":types.Default,
	"email":types.Email,
	"number":types.Number,
	"empty":types.Empty,
	"nonempty":types.NonEmpty,
	"hexcolor":types.HEXColor,
	"file":types.File
}
