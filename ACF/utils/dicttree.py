#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@marcin: docstrings
from ACF.utils.generations import *

def get(d,path,falseOnNotFound=True):
	"""
	Returns value from dict hierarchy.
	input: dict, path which is a list eg ['an', 'example', 'path'],
	returns: False or deepest found dict
	"""
	if type(d) is Generation:
		d=d.__dict__
	try:
		ret=d
		i=0
		for o in path:
			ret=ret[o]
			i+=1
	except (AttributeError, KeyError, TypeError):
		if falseOnNotFound:
			return False
		return (ret,i)
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
