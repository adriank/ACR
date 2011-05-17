#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ACR.utils.interpreter import *
import readline
from types import GeneratorType as generator

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

fakeEnv=FakeEnv()

print """AC Runtime BLSL Expression interactive shell
	This interpreter has one storage accessible through "rs" namespace.
	ctrl+c to exit.
"""
debug=True
try:
	while True:
		#try:
			tree=make_tree(raw_input(">>> "))
			if debug:
				print tree.tree
			r=tree.execute(fakeEnv)
			if type(r) is generator:
				if debug:
					print "returning generator"
				print list(r)
			else:
				print r
		#except Exception,e:
		#	print e
except KeyboardInterrupt:
	pass
#new line at the end forces command prompt to apear at left
print
