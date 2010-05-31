#!/usr/bin/env python
from ACF.components import *

def serialize(env):
	def rec(node,tab):
		if type(node) in [Object,List]:
			tag=node.__class__.__name__.lower()
			attrs=node.__dict__.copy()
			attrs.pop("_value")
			content=node._value
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
			for i in content:
				if type(i) in [tuple,Object,List]:
					rec(i,tab)
				elif type(i) is str:
					tab.append(i)
				else:
					tab.append(str(i))
			#	else:
			#		raise "type of "+str([i])+" is"+str(type(i))+"\n"+str(root)
			tab.append("</"+tag+">")
	#if D: log.info("Generating XML")
	tab=[]
	structure=env.generations
	for i in structure.values():
		rec(i,tab)
	xslt=""
	if env.output["xsltfile"]:
		xslt="""\n<?xml-stylesheet type="text/xsl" href="/xslt/%s"?>\n"""%env.output["xsltfile"]
	return """<?xml version="1.0" encoding="UTF-8"?>%s<list>%s</list>\n"""%(xslt,"".join(tab))
