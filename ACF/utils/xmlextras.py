#!/usr/bin/env python
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

#TODO; remove tpath
#@marcin: functions docstrings

from xml.sax import make_parser, handler
from ACF.errors import Error
from xml.sax.saxutils import escape,unescape
from ACF.components import Object,List
import re

RE_ATTR=re.compile("'([^']+)': '([^']*)',*")
D=False
unescapeDict={"&apos;":"'","&quot;":"\""}
escapeDict={"'":"&apos;","\"":"&quot;"}

class ObjectTree(tuple):
	def __init__(self,seq):
		tuple.__init__(seq)

	def get(self,path):
		return tpath(self,path)

#TO-C
def escapeQuotes(s):
	"""
	Escape characters '<', '>', '\'', '"', '&' in s
	input: string
	returns: string with escaped characters
	"""
	return escape(unescape(s,unescapeDict),escapeDict)

def str2obj(s):
	"""
	Converts string to an object.
	input: string
	returns: object which was converted or the same string's object representation as in input
	"""
	r=s.strip().lower()
	if r=="true" or r=="t":
		return True
	elif r=="false" or r=="f":
		return False
	elif r=="none":
		return None
	#TODO is that correct?
	return s

#TO-C
def tree2xml(root):
	"""
	Converts xml tree to a xml.
	input: xml tree
	returns: xml tree parsed to a xml
	"""
	def rec(node):
		if type(node) in [Object,List]:
			tag=node._name
			content=node._value
			attrs=node.__dict__#.copy()
			attrs.pop("_value")
		elif type(node) is tuple:
			tag=node[0]
			attrs=node[1]
			content=node[2]
		tab.append("<"+tag)
		if attrs and len(attrs)>0:
			tab.append(" "+RE_ATTR.sub(r'\1="\2"', str(attrs)[1:-1]))
		nodes=[]
		if not content:
			tab.append("/>")
		else:
			tab.append(">")
			typ=type(content)
			if typ is str:
				tab.append(content)
			#TODO this is probably wrong
			else:
				for i in content:
					typei=type(i)
					if typei is str:
						tab.append(i)
					elif typei in [tuple,Object,List,list]:
						rec(i)
					else:
						tab.append(str(i))
			#	else:
			#		raise "type of "+str([i])+" is"+str(type(i))+"\n"+str(root)
			tab.append("</"+tag+">")
	#if D: log.info("Generating XML")
	tab=[]
	rec(root)
	return "".join(tab)

#need to try whether xml.etree.cElementTree is faster here; pure Python etree is slower
class Reader(handler.ContentHandler):
	def __init__(self):
		self.root=None
		self.path=[]

	def startElement(self, name, a):
		attrs=None
		if len(a)>0:
			attrs={}
			for i in a.keys():
				attrs[str(i).lower()]=str2obj(str(a[i].strip()))
		if not len(self.path):
			self.root=ObjectTree([str(name).lower(),attrs,[]])
			self.path.append(self.root)
		else:
			l=self.path[-1]
			l[2].append((str(name).lower(),attrs,[]))
			self.path.append(l[2][-1])

	def characters(self,data):
		if len(data.strip())>0:
			self.path[-1][2].append(str2obj(data).encode("utf-8"))
		#TODO make it work with ANY whitespaces in XML files
		elif len(data)==1 and data[0] not in ["\t","\n"]:
			self.path[-1][2].append(" ")

	def endElement(self,x):
		subelems=[]
		lines=[]
		elem=self.path[-1][2]
		for i in elem:
			if type(i) is tuple:
				if len(lines):
					subelems.append("\n".join(lines))
					lines=[]
				subelems.append(i)
			elif type(i) is str:
				lines.append(i)
		if len(lines):
			subelems.append("\n".join(lines))
		elem[0:len(elem)]=subelems
		self.path.pop()

def xml2tree(xmlfile):
	"""
	Parses xml resource to xml tree.
	input: xml file or url resource
	returns: xml tree
	"""
	parser=make_parser()
	r=Reader()
	parser.setContentHandler(r)
	parser.parse(xmlfile)
	return r.root

def tpath(root,path):
	#print "path is "+path
	t=path.split("/")
	try:
		t.pop(0)
		ret=root
		if t:
			#print "t: "+str(t)
			for i in t:
				if type(ret) is list:
					ret=ret[0]
				#print i
				splitter=i.find("[")
				_filter=None
				if splitter>0:
					_filter=i[splitter+1:-1].strip()
					i=i[0:splitter]
				#print "ret: "+str(ret)
				if i=="*":
					ret=ret[2]
				if i=="text()":
					ret=list(filter(lambda x: type(x[0]) is str,ret[2]))
				else:
					tags=i.split("|")
					ret=list(filter(lambda x: x[0] in tags, ret[2]))
				if _filter:
					if _filter.isdigit():
						ret=ret[int(filter)]
					elif _filter[0] is "@":
						t=_filter[1:].split("=")
						if len(t)>1:
							ret=list(filter(lambda x: x[1].get(attr,"ERROR")==t[1],ret))[0]
						else:
							if t[0]=="*":
								return ret[0][1]
							return ret[0][1][t[0]]
				#print "done: "+str(ret)
	except (AttributeError, KeyError, TypeError,IndexError),e:
		return None
	return ret

def NS2Tuple(s,delimiter=":"):
	"""
	Distance namespace from its other part.
	input: xml-like namespace in a string
	returns: tuple (namespace: rest)
	"""
	try:
		ns,action=s.split(delimiter)
	except:
		ns,action=(None,s)
	return (ns,action)
