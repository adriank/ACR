#!/usr/bin/env python
# -*- coding: utf-8 -*-

# d is dict
# path is a list eg ['an', 'example', 'path']
# falseOnNotFound - return False or deepest found dict
# returns value from dict hierarchy
def get(d,path,falseOnNotFound=True):
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

# inserts object o into obj, path is a list , like above
# TODO add param for overwriting
def set(d, path, o):
	for key in path[:-1]:
		if not d.has_key(key) or type(d[key]) is not dict:
			d[key]={}
		d=d[key]
	d[path[-1]]=o

#TODO this is test for get and set. move to tests
#d={"a":1}
#set(d,["a","b","c"],1)
#print str(d)
#print get(d,["a","b"])
