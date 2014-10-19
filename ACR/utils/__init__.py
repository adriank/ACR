#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,time,random,base64,re
from datetime import datetime, timedelta
from ACR.errors import *
from ACR.utils.hashcompat import md5_constructor
from ACR.utils.xmlextras import escapeQuotes, py2JSON
from ACR.utils import *
#from ACR.utils import makeTree
from ACR.utils.timeutils import now
from ACR import acconfig
from types import GeneratorType as generator
from itertools import chain

iterators=[list,generator,chain]

if hasattr(random, 'SystemRandom'):
	randrange=random.SystemRandom().randrange
else:
	randrange=random.randrange

RE_PATH=re.compile("{\$([^}]+)}") # {$ foobar}
RE_PATH_split=re.compile("{\$[^}]+}") # {$ foobar}
RE_PATH_Mustashes=re.compile("{{(.+?)}}") # {{OPexpr}
RE_PATH_Mustashes_split=re.compile("{{.+?}}") # {{OPexpr}}

def skip(g,n):
	if type(n) is not int:
		raise TypeError("generator indices must be integers, not %s"%type(n).__name__)
	j=0
	for i in g:
		if j is n:
			return i
		j+=1
	raise IndexError("generator index out of range")

def chunks(l, n):
	""" Yield successive n-sized chunks from l.
	"""
	for i in xrange(0, len(l), n):
		yield l[i:i+n]

def getStorage(env,s):
	D=env.doDebug
	if D:
		env.start("getStorage with s= '%s'",s)
	s=s.lower()
	if s=="session" or s=="ss":
		if not env.sessionStorage:
			if D: env.end("getStorage with: session do not exists")
			return False
		if D: env.end("getStorage with: session storage")
		return env.sessionStorage.data
	if s=="env" or s=="env":
		return env.env
	#elif s=="app" or s=="as":
	#	return
	#TODO cookie storage
	#elif s=="cookie" or s=="cs":
	#	return
	elif s=="global" or s=="gs":
		return {}
	if D: env.end("getStorage with: request storage")
	return env.requestStorage

def replaceVars(env,l,fn=None):
	"""
	l - output of prepareVars
	fn - function that will be executed on each string
	"""
	D=env.doDebug
	if D: env.start("replaceVars with: path='%s' and fn='%s'", l, fn)
	try:
		l.__iter__
	except:
		return l
	ret=[]
	for i in l:
		if type(i) is interpreter.Tree:
			ret.append(str(i.execute(env)))
		elif type(i) is tuple:
			if D: env.debug("computing '%s'",i)
			storage=getStorage(env,i[0])
			v=py2JSON(dicttree.get(storage,i[1],acenv=env))
			if v in ("null","false"):
				continue
			if fn is not None:
				if type(v) is unicode:
					v=v.encode("utf8")
				v=fn(v)
			if D: env.debug("adding '%s' to the end of string",v)
			ret.append(v)
		else:
			if D: env.debug("adding '%s' to the end of string",i)
			if fn is not None:
				i=fn(i)
			ret.append(i)
	if len(ret) is 1 and ret:
		if D: env.debug("END replaceVars with: %s",ret[0])
		return ret[0]
	try:
#		ret=filter(map(lambda e: type(e) is unicode and e.encode("utf-8") or e,ret),lambda e:e not in (None,False))
		ret=map(lambda e: type(e) is unicode and e.encode("utf-8") or e,ret)
		if D: env.debug("END replaceVars with: %s","".join(ret))
		return "".join(ret)
	except TypeError,e:
		if D: env.error("END replaceVars with TypeError: %s; returning %s",e,ret)
		return ret

def prepareVars(s):
	if type(s) is not str:
		return s
	splitted=RE_PATH_split.split(s)
	variables=RE_PATH.findall(s)
	#print "splitted",splitted
	#print "variables",variables
	ret=[]
	STORAGES=["rs","ss","env","config"]
	try:
		while True:
			string=splitted.pop(0)
			splittedM=RE_PATH_Mustashes_split.split(string)
			variablesM=RE_PATH_Mustashes.findall(string)
			#print "splittedM",splittedM
			#print "variablesM",variablesM
			try:
				while True:
					ret.append(splittedM.pop(0))
					ret.append(interpreter.makeTree(variablesM.pop(0)))
			except IndexError:
				pass
			var=variables.pop(0)
			path=var.split(".")
			storageName=path.pop(0) or "rs"
			if storageName not in STORAGES:
				raise Exception("Wrong storage name in $%s. Should it be $.%s?"%(var,var))
			ret.append((storageName,path))
	except IndexError:
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

def str2obj(s):
	"""
		Converts string to an object.
		input: string
		returns: object which was converted or the same string's object representation as in input
	"""
	r=s.strip().lower()
	if r in ("true","t","y","yes"):
		return True
	elif r in ("false","f","no"):
		return False
	elif r in ("none","nil","null"):
		return None
	return s

from ACR.utils import actypes as types
typesMap={
	"default":types.Default,
	"text":types.Text,
	"xml":types.Default,
	"html":types.Default,
	"email":types.Email,
	"url":types.URL,
	"number":types.Number,
	"boolean":types.Boolean,
	"empty":types.Empty,
	"nonempty":types.NonEmpty,
	"hexcolor":types.HEXColor,
	"file":types.File,
	"csv":types.CSV,
	"array":types.List,
	"safehtml":types.safeHTML,
	"json":types.JSON
}
