#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO:
# prepare test without creating an instance of classes like appliaction or environment in order not to start server

from ACF.utils.tester import Tester
from ACF.core.environment import Environment
from ACF.core.application import Application
from ACF.utils import *
from ACF.session import *

# unit tests for functions: getStorage, objectPath, generateID, replaceVars

class myEnv:
	def __init__(self):
		self.requestStorage = False
		self.sessionStorage = None

def setUpEnv():
	global env
	env = myEnv()


def test_getStorage():
	env.sessionStorage = None
	assert getStorage(env, "Session") == False and getStorage(env, "ss") == False
	assert getStorage(env, "gs") == [] and getStorage(env, "global") == []
	# TODO test when sessionStorage is not None
	return True

def test_objectPath():
	d = {'x': {'y': 'z', 'a' : {'b': {'c' : {'d': 'e'}}}}, 'w': 't', 'r' : {'o' : 'l', 'g' : {'q': 's'}} }
	assert objectPath(d, 'x.y') == 'z'
	assert objectPath(d, 'x.a.b.c.d') == 'e'
	assert objectPath(d, 'w') == 't'
	assert objectPath(d, 'r.o') == 'l'
	assert objectPath(d, 'r.g.q') == 's'
	assert objectPath(d, 'x.y.z') == False
	assert objectPath(d, 'x.b') == False
	assert objectPath({'a': ['b','c']}, 'a') == False
	assert objectPath({'a': ['b','c']}, 'a.b') == False
	return True

def test_replaceVars():
	pass

def test_generateID():
	id = generateID()
	assert type(id) == str and len(id) == 32
	return True

def doTests():
	tester = Tester("utils.__init__")
	tester.addTest(test_getStorage).setUp(setUpEnv).addTest(test_objectPath).addTest(test_generateID,10)
	tester.run()