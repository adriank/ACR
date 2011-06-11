#!/usr/bin/env python

# code from http://effbot.org/zone/simple-top-down-parsing.htm
# licence of original code was public domain
# relicenced to AGPL v3 by Asyncode Ltd. and:
# - specialized to work with ACR,
# - added interpreter,
# - optimized

# !!!NOT THREAD SAFE!!!
#TODO thread safety!
import sys
import re
from cStringIO import StringIO
from ACR.utils import getStorage, dicttree, iterators, generator, chain, skip

class ProgrammingError(Exception):
	pass

symbol_table={}

#TODO optimization ('-',1) -> -1
#TODO optimization operators should be numbers

TRUE=["true","t"]
FALSE=["false","f"]
NONE=["none","null","n","nil"]

class symbol_base(object):
	id=None
	value=None
	fst=snd=third=None

	def nud(self):
		raise SyntaxError("Syntax error (%r)." % self.id)

	def led(self, left):
		raise SyntaxError("Unknown operator (%r)." % self.id)

	def getTree(self):
		if self.id == "(name)":
			val=self.value.lower()
			if val in TRUE:
				return True
			elif val in FALSE:
				return False
			elif val in NONE:
				return None
			return (self.id[1:-1], self.value)
		elif self.id == "(literal)":
			fstLetter=self.value[0]
			if fstLetter in ["'","\""]:
				return self.value[1:-1]
			elif fstLetter.isdigit():
				try:
					return int(self.value)
				except:
					return float(self.value)
			else:
				if self.value=="True":
					return True
				elif self.value=="False":
					return False
				elif self.value=="None":
					return None
		#XXX this is crap - don't know where I've took this from
		out=[self.id, self.fst, self.snd, self.third]
		ret=[]
		ret_append=ret.append
		L=[dict,tuple,list]
		for i in filter(None, out):
			if type(i) is str:
				ret_append(i)
			elif type(i) in L:
				t=[]
				t_append=t.append
				if self.id is "{":
					ret={}
					for j in self.fst.iteritems():
						ret[j[0].getTree()]=j[1].getTree()
					return ret
				for j in i:
					try:
						t_append(j.getTree())
					except:
						t_append(j)
				if self.id is "(":
					if len(t) is 1:
						t=t[0]
					return (self.id,ret[1],t)
				#TODO check if this is ever used?
				if self.id is "[":
					return t
				#ret_append(t)
				#return (self.id,ret[1:])
			else:
				ret_append(i.getTree())
		return tuple(ret)

	def __repr__(self):
		if self.id == "(name)" or self.id == "(literal)":
			return "(%s %s)" % (self.id[1:-1], self.value)
		out=[self.id, self.fst, self.snd, self.third]
		out=map(str, filter(None, out))
		return "(" + " ".join(out) + ")"

def symbol(id, bp=0):
	try:
		s=symbol_table[id]
	except KeyError:
		class s(symbol_base):
			pass
		s.__name__="symbol-" + id # for debugging
		s.id=id
		s.value=None
		s.lbp=bp
		symbol_table[id]=s
	else:
		s.lbp=max(bp, s.lbp)
	return s

# helpers

def infix(id, bp):
	def led(self, left):
		self.fst=left
		self.snd=expression(bp)
		return self
	symbol(id, bp).led=led

def infix_r(id, bp):
	def led(self, left):
		self.fst=left
		self.snd=expression(bp-1)
		return self
	symbol(id, bp).led=led

def prefix(id, bp):
	def nud(self):
		self.fst=expression(bp)
		return self
	symbol(id).nud=nud

def advance(id=None):
	global token
	if id and token.id != id:
		raise SyntaxError("Expected %r, got %s"%(id,token.id))
	token=next()

def method(s):
	# decorator
	assert issubclass(s, symbol_base)
	def bind(fn):
		setattr(s, fn.__name__, fn)
	return bind

infix_r("or", 30); infix_r("and", 40); prefix("not", 50)
infix("in", 60); infix("not", 60) # not in
infix("is", 60);
infix("<", 60); infix("<=", 60)
infix(">", 60); infix(">=", 60)
#infix("<>", 60); infix("!=", 60); infix("==", 60)
#infix("|", 70); infix("^", 80); infix("&", 90)
#infix("<<", 100); infix(">>", 100)
infix("+", 110); infix("-", 110)
infix("*", 120); infix("/", 120); infix("//", 120)
infix("%", 120)
prefix("-", 130); prefix("+", 130); #prefix("~", 130)
#infix_r("**", 140)
symbol(".", 150); symbol("[", 150); symbol("(", 150)
# additional behaviour
symbol("(name)").nud=lambda self: self
symbol("(literal)").nud=lambda self: self
symbol("(end)")
symbol(")")

symbol("@")
@method(symbol("@"))
def nud(self):
	self.id="(current)"
	return self

@method(symbol("("))
def nud(self):
	expr=expression()
	advance(")")
	return expr

@method(symbol("."))
def led(self, left):
	attr=False
	if token.id is ".":
		self.id=".."
		advance()
	if token.id is "@":
		attr=True
		advance()
	if token.id not in ["(name)","*" ]:
		raise SyntaxError("Expected an attribute name.")
	self.fst=left
	if attr:
		token.value="@"+token.value
	self.snd=token
	advance()
	return self

#handling storages; e.g $.a.b.c or $ss.a.b.c
#default storage is request storage
symbol("$")
@method(symbol("$"))
def nud(self):
	global token
	self.id="(storage)"
	if token.id is ".":
		self.fst="rs"
	else:
		self.fst=token.value
		advance()
	return self

symbol("]")

@method(symbol("["))
def led(self, left):
	self.fst=left
	self.snd=expression()
	advance("]")
	return self

symbol(",")

#this is for built-in functions
@method(symbol("("))
def led(self, left):
	self.fst=left
	self.snd=[]
	if token.id is not ")":
		self_snd_append=self.snd.append
		while 1:
			self_snd_append(expression())
			if token.id is not ",":
				break
			advance(",")
	advance(")")
	return self

symbol(":")
symbol("=")

# constants

def constant(id):
	@method(symbol(id))
	def nud(self):
		self.id="(literal)"
		self.value=id
		return self

constant("None")
constant("True")
constant("False")

#multitoken operators

@method(symbol("not"))
def led(self, left):
	if token.id != "in":
		raise SyntaxError("Invalid syntax")
	advance()
	self.id="not in"
	self.fst=left
	self.snd=expression(60)
	return self

@method(symbol("is"))
def led(self, left):
	if token.id == "not":
		advance()
		self.id="is not"
	self.fst=left
	self.snd=expression(60)
	return self

symbol("]")

@method(symbol("["))
def nud(self):
	self.fst=[]
	if token.id is not "]":
		while 1:
			if token.id is "]":
				break
			self.fst.append(expression())
			if token.id not in SELECTOR_OPS+[","]:
				break
			advance(",")
	advance("]")
	return self

symbol("}")

@method(symbol("{"))
def nud(self):
	self.fst={}
	if token.id is not "}":
		while 1:
			if token.id is "}":
				break
			key=expression()
			advance(":")
			self.fst[key]=expression()
			if token.id is not ",":
				break
			advance(",")
	advance("}")
	return self

import tokenize as tokenizer
type_map={
	tokenizer.NUMBER:"(literal)",
	tokenizer.STRING:"(literal)",
	tokenizer.OP:"(operator)",
	tokenizer.NAME:"(name)",
	tokenizer.ERRORTOKEN:"(operator)" #'$' is recognized in python tokenizer as error token!
}

# python tokenizer
def tokenize_python(program):
	for t in tokenizer.generate_tokens(StringIO(program).next):
		try:
			#change this to output python values in correct type
			yield type_map[t[0]], t[1]
		except KeyError:
			if t[0] == tokenizer.NL:
				continue
			if t[0] == tokenizer.ENDMARKER:
				break
			else:
				raise SyntaxError("Syntax error")
	yield "(end)", "(end)"

def tokenize(program):
	if isinstance(program, list):
		source=program
	else:
		source=tokenize_python(program)
	for id, value in source:
		if id=="(literal)":
			symbol=symbol_table[id]
			s=symbol()
			s.value=value
		elif value is " ":
			continue
		else:
			# name or operator
			symbol=symbol_table.get(value)
			if symbol:
				s=symbol()
			#elif id==" ":
			elif id=="(name)":
				symbol=symbol_table[id]
				s=symbol()
				s.value=value
			else:
				raise SyntaxError("Unknown operator '%s', '%s'" % (id,value))
		yield s

# parser engine
def expression(rbp=0):
	global token
	t=token
	token=next()
	left=t.nud()
	while rbp < token.lbp:
		t=token
		token=next()
		left=t.led(left)
	return left

def make_tree(expr):
	if type(expr) is not str:
		return Tree(expr)
	expr=expr.strip()
	if not len(expr):
		return Tree(True)
	global token, next
	next=tokenize(expr).next
	token=next()
	return Tree(expression().getTree())

SELECTOR_OPS=["is",">","<","is not",">=","<=","in","not in",":"]
#it must be list because of further concatenations
NUM_TYPES=[int,float,long]
STR_TYPES=[str,unicode]
ITER_TYPES=iterators

#setting external modules to 0, thus enabling lazy loading. 0 ensures that Pythonic types are never matched.
#this way is efficient because if statement is fast and once loaded these variables are pointing to libraries.
timeutils=ObjectId=generateID=calendar=escape=escapeDict=unescape=unescapeDict=0

class Tree(object):
	def __init__(self,tree):
		self.tree=tree

	def execute(self,acenv):
		D=acenv.doDebug
		if D: acenv.start("Tree.execute")
		#TODO change to yield?
		def exe(node):
			"""
				node[0] - operator name
				node[1:] - params
			"""
			if D: acenv.debug("executing node '%s'", node)
			type_node=type(node)
			if node is None or type_node in (str,int,float,long,bool,generator,chain):
				return node
			elif type_node is list:
				return map(exe,node)
			elif type_node is dict:
				ret={}
				for i in node.iteritems():
					ret[exe(i[0])]=exe(i[1])
				return ret
			op=node[0]
			if op=="or":
				if D: acenv.debug("%s or %s", exe(node[1]),exe(node[2]))
				return exe(node[1]) or exe(node[2])
			elif op=="and":
				if D: acenv.debug("%s and %s", exe(node[1]),exe(node[2]))
				return exe(node[1]) and exe(node[2])
			elif op=="+":
				if len(node)>2:
					fst=exe(node[1])
					snd=exe(node[2])
					typefst=type(fst)
					if typefst is dict:
						fst.update(snd)
						return fst
					typesnd=type(snd)
					if typefst in ITER_TYPES or typesnd in ITER_TYPES:
						return chain(fst,snd)
					if typefst in STR_TYPES or typesnd in STR_TYPES:
						if D: acenv.info("doing string comparison '%s' is '%s'",fst,snd)
						return str(fst)+str(snd)
					return fst + snd
				else:
					return exe(node[1])
			elif op=="-":
				#TODO move -N to tree builder!
				if len(node)>2:
					return exe(node[1]) - exe(node[2])
				else:
					return - exe(node[1])
			elif op=="*":
				return exe(node[1]) * exe(node[2])
			elif op=="%":
				return exe(node[1]) % exe(node[2])
			elif op=="/":
				return exe(node[1]) / float(exe(node[2]))
			elif op==">":
				return exe(node[1]) > exe(node[2])
			elif op=="<":
				return exe(node[1]) < exe(node[2])
			elif op==">=":
				return exe(node[1]) >= exe(node[2])
			elif op=="<=":
				return exe(node[1]) <= exe(node[2])
			#TODO this algorithm produces 3 for 1<2<3 and should be true
			#elif op in "<=>=":
			#	fst=exe(node[1])
			#	snd=exe(node[2])
			#	if op==">":
			#		return fst > snd and snd or False
			#	elif op=="<":
			#		return fst < snd and snd or False
			#	elif op==">=":
			#		return fst >= snd and snd or False
			#	elif op=="<=":
			#		return fst <= snd and snd or False
			elif op=="not":
				fst=exe(node[1])
				if D: acenv.debug("doing not '%s'",fst)
				return not fst
			elif op=="in":
				if D: acenv.debug("doing '%s' in '%s'",exe(node[1]),exe(node[2]))
				return exe(node[1]) in exe(node[2])
			elif op=="not in":
				return exe(node[1]) not in exe(node[2])
			elif op in ("is","is not"):
				if D: acenv.debug("found operator '%s'",op)
				fst=exe(node[1])
				snd=exe(node[2])
				typefst=type(fst)
				typesnd=type(snd)
				if typefst in STR_TYPES:
					if D: acenv.info("doing string comparison '%s' is '%s'",fst,snd)
					ret=fst==str(snd)
				elif typefst is float:
					if D: acenv.info("doing float comparison '%s' is '%s'",fst,snd)
					ret=fst==float(snd)
				elif typefst is int:
					if D: acenv.info("doing float comparison '%s' is '%s'",fst,snd)
					ret=fst==int(snd)
				elif typefst is list and typesnd is list:
					ret=fst==snd
				elif typefst is dict and typesnd is dict:
					ret=fst==snd
				else:
					if D: acenv.info("doing standard comparison '%s' is '%s'",fst,snd)
					ret=fst is snd
				if op=="is not":
					if D: acenv.info("'is not' found. Returning %s",not ret)
					return not ret
				else:
					return ret
			elif op=="(literal)":
				fstLetter=node[1][0]
				if fstLetter is "'":
					return node[1][1:-1]
				elif fstLetter.isdigit:
					return int(node[1])
			elif op=="(storage)":
				return getStorage(acenv,node[1])
			elif op=="(current)":
				return self.current
			elif op=="name":
				return node[1]
			elif op==".":
				fst=node[1]
				if type(fst) is tuple:
					fst=exe(fst)
				typefst=type(fst)
				if D: acenv.debug("left is '%s'",fst)
				if node[2][0]=="*":
					return typefst in ITER_TYPES and fst or [fst]
				snd=exe(node[2])
				if D: acenv.debug("right is '%s'",snd)
				if typefst in ITER_TYPES:
					ret=[]
					ret_append=ret.append
					for i in fst:
						try:
							ret_append(i[snd])
						except:
							pass
					return ret
				try:
					return fst.get(snd)
				except:
					return fst
			elif op=="..":
				fst=dicttree.flatten(exe(node[1]))
				if node[2][0]=="*":
					return fst
				ret=[]
				snd=exe(node[2])
				for i in fst:
					try:
						ret.append(i[snd])
					except:
						pass
				return ret
			#TODO move it to tree generation phase
			elif op=="{":
				return {}
			elif op=="[":
				len_node=len(node)
				#TODO move it to tree generation phase
				if len_node is 1: # empty list
					return []
				if len_node is 2: # list - preserved to catch possible event of leaving it as '[' operator
					#TODO yielding is not possible here
					#if type(node[1]) in (generator,chain):
					#	for i in node[1]:
					#		yield exe(i)
					return map(exe,node[1])
				if len_node is 3: # operator []
					fst=exe(node[1])
					if not fst:
						return fst
					s=node[2]
					if type(s) is tuple and s[0] in SELECTOR_OPS:
						nodeList=[]
						nodeList_append=nodeList.append
						for i in fst:
							self.current=i
							#TODO move it to tree building phase
							if type(s[1]) is tuple and s[1][0]=="name":
								s=(s[0],s[1][1],s[2])
							if type(s[1]) in STR_TYPES:
								try:
									if exe((s[0],i[s[1]],s[2])):
										nodeList_append(i)
								except:
									pass
							else:
								try:
									#TODO optimize an event when @ is not used. exe(s[1]) can be cached
									if exe((s[0],exe(s[1]),exe(s[2]))):
										nodeList_append(i)
								except:
									pass
						return nodeList
					snd=exe(node[2])
					tfst=type(fst)
					if tfst in [tuple]+ITER_TYPES+STR_TYPES:
						# nodes[N]
						if type(snd) in NUM_TYPES or snd.isdigit():
							n=int(snd)
							if tfst in (generator,chain):
								if n>0:
									return skip(fst,n)
								elif n==0:
									return fst.next()
								else:
									fst=list(fst)
							else:
								return fst[n]
						return exe((".",fst,snd))
					else:
						try:
							return fst[snd]
						except:
							return []
				raise ProgrammingError("Wrong usage of '[' operator")
			elif op=="(":
				""" Built-in functions """
				fnName=node[1][1]
				args=None
				try:
					args=exe(node[2])
				except:
					pass
				#arithmetic
				if fnName=="sum":
					if type(args) in NUM_TYPES:
						return args
					return sum(map(lambda x:type(x) in NUM_TYPES and x or exe(x), args))
				elif fnName=="max":
					if type(args) in NUM_TYPES:
						return args
					return max(map(lambda x:type(x) in NUM_TYPES and x or exe(x), args))
				elif fnName=="min":
					if type(args) in NUM_TYPES:
						return args
					return min(map(lambda x:type(x) in NUM_TYPES and x or exe(x), args))
				elif fnName=="round":
					if type(args) is list:
						return round(*args)
					return round(args)
				#casting
				elif fnName=="int":
					return int(args)
				elif fnName=="float":
					return float(args)
				elif fnName=="str":
					return str(args)
				#string
				elif fnName=="escape":
					global escape,escapeDict
					if not escape:
						from ACR.utils.xmlextras import escape, escapeDict
					return escape(args,escapeDict)
				elif fnName=="unescape":
					global unescape,unescapeDict
					if not unescape:
						from ACR.utils.xmlextras import unescape, unescapeDict
					return unescape(args,unescapeDict)
				elif fnName=="replace":
					if type(args[0]) is unicode:
						args[0]=args[0].encode("utf8")
					return str.replace(args[0],args[1],args[2])
				elif fnName=="REsub":
					return re.sub(args[1],args[2],args[0])
				#array
				elif fnName=="sort":
					if type(args) in (generator,chain):
						args=list(args)
					args.sort()
					return args
				elif fnName=="reverse":
					if type(args) in (generator,chain):
						args=list(args)
					#reversed() is not help here since either way all data should be put in RAM and then reversed
					args.reverse()
					return args
				elif fnName in ("count","len"):
					if args in (True,False,None):
						return args
					if type(args) in ITER_TYPES:
						return len(list(args))
					return len(args)
				#time
				elif fnName in ("now","age"):
					global timeutils
					if not timeutils:
						from ACR.utils import timeutils
					if fnName=="now":
						return timeutils.now()
					if fnName=="age":
						return timeutils.age(args,getStorage(acenv,"rs")["__lang__"])
				elif fnName=="toMillis":
					if args.utcoffset() is not None:
						args=args-args.utcoffset()
					global calendar
					if not calendar:
						import calendar
					return int(calendar.timegm(args.timetuple()) * 1000 + args.microsnd / 1000)
				#misc
				elif fnName=="type":
					ret=type(args)
					if ret in ITER_TYPES:
						return "array"
					if ret is dict:
						return "object"
					return ret.__name__
				elif fnName=="generateID":
					global generateID
					if not generateID:
						from ACR.utils import generateID
					return generateID()
				elif fnName in ("objectID","ObjectId"):
					global ObjectId
					if not ObjectId:
						from bson.objectid import ObjectId
					return ObjectId(args)
				else:
					raise ProgrammingError("Function '"+fnName+"' does not exist.")
			else:
				return node

		D=acenv.doDebug
		if type(self.tree) not in (tuple,list,dict):
			return self.tree
		ret=exe(self.tree)
		if D: acenv.end("Tree.execute with: '%s'", ret)
		return ret

	def __str__(self):
		return "TreeObject(%s)"%str(self.tree)

	def __repr__(self):
		return self.__str__()
