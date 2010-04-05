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

from xml.sax import make_parser, handler
from ACF.errors import Error
from xml.sax.saxutils import escape,unescape
import logging,re

RE_ATTR=re.compile("u?'([^']+)': u?'([^']*)',*")
log=logging.getLogger('ACF.utils.xmlextras')
D=logging.doLog
unescapeDict={"&apos;":"'","&quot;":"\""}
escapeDict={"'":"&apos;","\"":"&quot;"}

class ObjectTree(tuple):
	def __init__(self,seq):
		tuple.__init__(seq)

	def get(self,path):
		return tpath(self,path)

def escapeQuotes(s):
	return escape(unescape(s,unescapeDict),escapeDict)

def str2obj(s):
	r=s.lower().strip()
	if r=="true" or r=="t":
		return True
	elif r=="false" or r=="f":
		return False
	elif r=="none":
		return None
	return s

def tree2xml(root):
	#TODO check if it can be changed into regexp
	if D: log.debug("Executing with root=%s",root)
	def rec(node,tab):
		tab.append("<"+node[0])
		if node[1] and len(node[1])>0:
			#print str(node[1])
			tab.append(" "+RE_ATTR.sub(r'\1="\2"', str(node[1])[1:-1]))
			#n=node[1]
			#for i in n:
			#	val=n[i]
			#	if type(val) is not str:
			#		val=str(val)
			#	tab.append(' '+i+'="'+val+'"')
		nodes=[]
		if not node[2]:
			tab.append("/>")
		else:
			tab.append(">")
			for i in node[2]:
				if type(i) is tuple:
					rec(i,tab)
				elif type(i) in [str,unicode]:
					tab.append(i)
				else:
					tab.append(unicode(i))
			#	else:
			#		raise "type of "+str([i])+" is"+str(type(i))+"\n"+str(root)
			tab.append("</"+node[0]+">")

	tab=[]
	rec(root,tab)
	#print round((time.time()-a)*1000,2)
	if D: log.debug("Returning tab=%s",tab)
	return "".join(tab)

#gives last item of any iterable object
def last(iterable):
	return iterable[len(iterable)-1]

#need to try whether xml.etree.cElementTree is faster here pure Python etree is slower
class Reader(handler.ContentHandler):
	def __init__(self):
		self.root=None
		self.path=[]

	def startElement(self, name, a):
		attrs=None
		if len(a)>0:
			attrs={}
			for i in a.keys():
				attrs[i.lower()]=str2obj(a[i].strip())
		if not len(self.path):
			self.root=ObjectTree([name.lower(),attrs,[]])
			self.path.append(self.root)
		else:
			l=last(self.path)
			l[2].append((name.lower(),attrs,[]))
			self.path.append(last(l[2]))

	def characters(self,data):
		if len(data.strip())>0:
			last(self.path)[2].append(str2obj(data))

	def endElement(self,x):
		subelems=[]
		lines=[]
		elem=last(self.path)[2]
		for i in elem:
			if type(i) is tuple:
				if len(lines):
					subelems.append("\n".join(lines))
					lines=[]
				subelems.append(i)
			elif type(i) in [str,unicode]:
				lines.append(i)
		if len(lines):
			subelems.append("\n".join(lines))
		elem[0:len(elem)]=subelems
		self.path.pop()

def xml2tree(xmlfile):
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
				splitter=i.find("[")
				_filter=None
				if splitter>0:
					_filter=i[splitter+1:-1].strip()
					i=i[0:splitter]
				#print "ret: "+str(ret)
				if i=="*":
					ret=ret[2]
				if i=="text()":
					ret=list(filter(lambda x: type(x[0]) in [str,unicode], ret[2]))
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
	try:
		ns,action=s.split(delimiter)
	except:
		ns,action=(None,s)
	return (ns,action)
