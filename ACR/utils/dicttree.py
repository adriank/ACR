#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Asyncode Runtime - XML framework allowing developing internet
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.#@marcin: docstrings

def get(d,path,falseOnNotFound=True,acenv=False):
	"""
	Returns value from dict/object hierarchy.
	input: dict, path which is a list eg ['an', 'example', 'path'],
	returns: False or deepest dict/object found
	"""
	#if isinstance(d, Generation):
	#	d=d.__dict__
	D=acenv and acenv.doDebug
	if D: acenv.debug("START dicttree.get with: \n\tdict='%s'\n\tpath='%s'\n\tfalseOnNotFound=%s",d,path,falseOnNotFound)
	try:
		ret=d
		i=0
		for o in path:
			if o[0]=="@":
				ret=getattr(ret, o[1:])
				break
			else:
				ret=ret[o]
				i+=1
	except (AttributeError, KeyError, TypeError):
		if D: acenv.debug("END dicttree.get with: ValueNotFound.")
		if falseOnNotFound:
			return False
		return (ret,i)
	if D: acenv.debug("END dicttree.get with: returning '%s'.", ret)
	if falseOnNotFound:
		return ret
	return (ret, i)

# TODO add param for overwriting
def set(d, path, o):
	"""
	Inserts object o into dict d.
	input: dict, path which is a list eg ['an', 'example', 'path'], object might be inserted into d
	returns: None
	"""
	for key in path[:-1]:
		if not d.has_key(key) or type(d[key]) is not dict:
			d[key]={}
		d=d[key]
	d[path[-1]]=o

#TODO implement limit function
def flatten(fragment,limit=False):
	def rec(frg):
		dtype=type(frg)
		if dtype is list:
			for i in frg:
				rec(i)
		elif dtype is dict:
			ret.append(frg)
			for i in frg.iteritems():
				rec(i[1])
	ret=[]
	rec(fragment)
	return ret
