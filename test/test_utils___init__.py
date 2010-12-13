#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@marcin: tests for functions getStorage, generateID

from ACR.utils import *
import unittest

class myEnv:
	def __init__(self):
		self.requestStorage = False
		self.sessionStorage = None

class Utils_init(unittest.TestCase):
	def setUp(self):
		self.env = myEnv()

	def test_getStorage(self):
		self.env.sessionStorage = None
		self.assertTrue(getStorage(self.env, "Session") == False and getStorage(self.env, "ss") == False)
		self.assertTrue(not getStorage(self.env, "gs") and not getStorage(self.env, "global"))

	# TODO 
	def test_replaceVars(self):
		pass
	
	def test_generateID(self):
		id = generateID()
		self.assertTrue(type(id) == str and len(id) == 32)
