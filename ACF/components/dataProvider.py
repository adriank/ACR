#!/usr/bin/env python

import pg
class queryobj:
	def __init__(self):
		self.columns=["*"]
		self.table=""
		self.conditions={}
		self.limit=None
		self.offset=None

def parseConfig(root):
	conditions={}
	attributes=[]
	for node in root.childNodes:
		if node.nodeName=="conditions":
			for attr in node.attributes.keys():
				conditions[attr]=node.attributes[attr].value
		elif node.nodeName=="attributes":
			for node2 in node.childNodes:
				attributes.append(node2.firstChild.data)
#		elif i.nodeName=="properties":
	return conditions

def init():
	return
