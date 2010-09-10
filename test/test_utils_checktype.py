#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@marcin: tests for functions: checkType

import unittest
from ACF.utils.checktype import *

class Utils_checktype(unittest.TestCase):
	def test_number(self):
		self.assertTrue(checkType('number', '2222'))
		self.assertTrue(checkType('number', '1224'))
		self.assertTrue(checkType('number', '023233'))
		self.assertTrue(not checkType('number', '-023233'))
		self.assertTrue(not checkType('number', '23233.2'))
		self.assertTrue(not checkType('number', ''))
		
	def test_text(self):
		self.assertTrue(checkType('text', 'example text'))
		self.assertTrue(checkType('text', '2 is the best of all'))
		self.assertTrue(not checkType('text', ''))
		self.assertTrue(not checkType('text', '	     '))
	
	def test_email(self):
		self.assertTrue(checkType('email', 'sb@sth.com'))
		self.assertTrue(checkType('email', 'sb.na@sth.com'))
		self.assertTrue(checkType('email', '%ss@sth.com'))
		self.assertTrue(not checkType('email', '/ss@sth.com'))
		self.assertTrue(not checkType('email', 's\\@sth.com'))
		self.assertTrue(not checkType('email', '%s@s@sth.com'))
		self.assertTrue(not checkType('email', 'a@sth.c'))
		self.assertTrue(not checkType('email', 'a@s'))
		self.assertTrue(not checkType('email', 'foo@bat'))
		
	def test_password(self):
		self.assertTrue(checkType('password', 'tr3@5ur3'))
		self.assertTrue(not checkType('password', ''))
	
	def test_csv(self):
		self.assertTrue(not checkType('csv', ''))
		self.assertTrue(not checkType('csv', '      '))
		self.assertTrue(checkType('csv', ' jjjjjj     '))
		