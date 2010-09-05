#!/usr/bin/env python
# -*- coding: utf-8 -*-

#returns value from dict hierarchy based on "a.b.c" paths
# path is a list eg ['an', 'example', 'path']
def getObject(obj,path,exception=True):
	try:
		ret=obj
		i=0
		for o in path:
			ret=ret[o]
			i+=1
	except (AttributeError, KeyError, TypeError):
		#if D: log.warning("%s",e)
		if exception:
			return False
		return (ret,i)
	if exception:
		return ret
	return (ret, i)

# inserts object o into obj, path is a list , like above
def setObject(obj, path, o):
	d=obj
	for key in path[:-1]:
		if not d.has_key(key):
			d[key]={}
		d=d[key]
	d[path[-1]] = o
