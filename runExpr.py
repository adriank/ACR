#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ACR.utils.interpreter import *
import readline,sys
from types import GeneratorType as generator
from itertools import chain

class FakeEnv(object):
	requestStorage={
		"test":{
			"_id":1,
			"name":"aaa",
			"o":{
				"_id":2
			},
			"l":[
				{
					"_id":3,
					"aaa":"ddd",
					"false":2
				},
				{
					"_id":4
				}
			]
		}
	}
	doDebug=False
	env={"lang":"pl"}
	def debug(*a):
		print a[1]%tuple(a[2:])
	def start(*a):
		print a[1]%tuple(a[2:])
	def end(*a):
		print a[1]%tuple(a[2:])
	def info(*a):
		print a[1]%tuple(a[2:])

fakeEnv=FakeEnv()

print """AC Runtime BLSL Expression interactive shell
	This interpreter has one storage accessible through "rs" namespace.
	ctrl+c to exit.
"""
fakeEnv.doDebug=True
try:
	while True:
		#try:
			if len(sys.argv) is 2:
				tree=makeTree(sys.argv[1])
			else:
				tree=makeTree(raw_input(">>> "))
			if fakeEnv.doDebug:
				print tree.tree
			r=tree.execute(fakeEnv)
			if type(r) in (generator,chain):
				if fakeEnv.doDebug:
					print "returning",type(r).__name__
				print list(r)
			else:
				print r
			if len(sys.argv) is 2:
				break
		#except Exception,e:
		#	print e
except KeyboardInterrupt:
	pass
#new line at the end forces command prompt to apear at left
print
