#!/usr/bin/env python

import acconfig
import sys
import cPickle

def get(name):
	try:
		file=open(acconfig.installDir+"/cache/"+name+".dump","r")
		return cPickle.load(file)
	except IOError:
		return False
	finally:
		close(file)

def add(obj):
	try:
		file=open(acconfig.installDir+"/cache/"+name+".dump","w")
		return cPickle.dump(obj,file,2)
	except IOError:
		return False
	finally:
		close(file)
