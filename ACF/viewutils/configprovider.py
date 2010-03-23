#!/usr/bin/python
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


from ACF import globals
from ACF.errors import *
#from ACF.utils import conditionchecker
from ACF.utils.xmlextras import *
from xml.dom import minidom

class ViewNotFound(Exception):
	pass

def parseView(viewName):
	"""
	returns dictionary:
	{
		"inputs": [
			{"name":val, "type":val, "default":val}
		],
		"configs": [
			{"component":val,"name":val, "config":val}
		],
		"post":[
			{"name":val}
		]
	}
	"""
	def parseInput(node):
		if not node.attributes.has_key("name"):
			raise Error("ViewDefinitionError","input element have to have attribute \"name\"")
		r={
			"name":str(node.attributes["name"].value),
			"default":None,
			"type":None
		}
		if node.attributes.has_key("default"):
			r["default"]=str(node.attributes["default"].value)
		if node.attributes.has_key("type"):
			r["type"]=str(node.attributes["type"].value)
		if node.attributes.has_key("re"):
			r["re"]=str(node.attributes["re"].value)
		return r

	try:
		tree=xml2tree(globals.appDir+"views/"+viewName+".xml")
	except IOError,e:
		raise ViewError("Suplied view not found")
	except:
		raise ViewError("Error in view file")
	inputs=[]
	resources=[]
	post=[]
	conditions=[]
	output=None
	# should implement checking of node names
	inputs=tpath(tree,"view.inputs")
	for n in root.childNodes:
		if n.nodeName.lower()=="inputs":
			for node in n.childNodes:
				if node.nodeName.lower()=="input":
					inputs.append(parseInput(node))
				elif node.nodeName.lower()=="post":
					post.append(parseInput(node))
		elif n.nodeName.lower()=="actions":
			for node in n.childNodes:
				if node.nodeType is not node.ELEMENT_NODE or node.nodeName!="action":
					continue
				name="ACF.components."+str(node.attributes["component"].value)
				__import__(name)
				import sys
				resource=sys.modules[name]
				name=None
				if node.attributes.has_key("name"):
					name=str(node.attributes["name"].value)
				resources.append({
					"name":name,
					"component":str(node.attributes["component"].value),
					"config":resource.parseConfig(node)
				})
		elif n.nodeName.lower()=="conditions":
			for node in n.childNodes:
				if node.nodeType==node.ELEMENT_NODE and node.nodeName.lower()=="condition":
					conditions.append(conditionchecker.parseConfig(node))
		elif n.nodeName.lower()=="output":
			output=str(n.attributes["format"].value)
	return {
		"inputs":inputs,
		"configs":resources,
		"post":post,
		"conditions":conditions,
		"output":output
	}
