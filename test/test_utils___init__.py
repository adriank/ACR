#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@marcin: tests for functions getStorage, generateID

from ACR.utils import *
import unittest

class myEnv:
	def __init__(self):
		self.requestStorage = False
		self.sessionStorage = None
		self.doDebug=False

class Utils_init(unittest.TestCase):
	def setUp(self):
		self.env = myEnv()

	def test_str2obj(self):
		self.assertTrue(str2obj('True') == True and str2obj('true') == True and str2obj('t') == True and str2obj('T') == True)
		self.assertTrue(str2obj('False') == False and str2obj('false') == False and str2obj('f') == False and str2obj('F') == False)
		self.assertTrue(str2obj('None') == None and str2obj('none') == None)
		self.assertTrue(str2obj('    false    ') == False)
		self.assertTrue(str2obj('[2, 3, 4]') == '[2, 3, 4]' and str2obj('{}') == '{}')

	def test_getStorage(self):
		self.env.sessionStorage = None
		self.assertTrue(getStorage(self.env, "Session") == False and getStorage(self.env, "ss") == False)
		self.assertTrue(not getStorage(self.env, "gs") and not getStorage(self.env, "global"))

	# TODO
	def test_replaceVars(self):
		pass

	def test_prepareVars(self):
		pass
		#prepareVars("ddd {{aaa}} bbb {$.sss} ccc")

	def test_generateID(self):
		id = generateID()
		self.assertTrue(type(id) == str and len(id) == 32)
