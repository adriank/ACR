#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ACR.utils.interpreter import *
class FakeEnv(object):
	requestStorage={}
	doDebug=False

fakeEnv=FakeEnv()

print """AC Runtime BLSL Expression interactive shell
	This interpreter has one storage accessible through "rs" namespace.
	ctrl+c to exit.
"""

try:
	while True:
		print make_tree(raw_input(">>> ")).execute(fakeEnv)
except KeyboardInterrupt:
	pass
