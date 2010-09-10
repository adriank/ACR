#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@marcin: unit tests for functions: dicttree.get, dicttree.set

from ACF.utils import dicttree
import unittest

class Utils_dicttree(unittest.TestCase):
	def test_dicttree_get(self):
		d = {'x': {'y': 'z', 'a' : {'b': {'c' : {'d': 'e'}}}}, 'w': 't', 'r' : {'o' : 'l', 'g' : {'q': 's'}} }
		self.assertTrue( dicttree.get(d, ['x', 'y'], False) == ('z', 2))
		self.assertTrue( dicttree.get(d, 'x.a.b.c.d'.split('.'), False) == ('e', 5))
		self.assertTrue( dicttree.get(d, 'x.a.b.c.d'.split('.')) == 'e')
		self.assertTrue( dicttree.get(d, ['w'], False) == ('t', 1))
		self.assertTrue( dicttree.get(d, 'r.o'.split('.'), False) == ('l', 2))
		self.assertTrue( dicttree.get(d, 'r.g.q'.split('.'), False) == ('s', 3))
		self.assertTrue( not dicttree.get(d, 'x.y.z'.split('.')))
		self.assertTrue( not dicttree.get(d, 'x.b'.split('.')))
		self.assertTrue( dicttree.get(d, ['r', 'g']) ==  {'q': 's'})
		self.assertTrue( dicttree.get(d, ['x', 'a', 'b'], False) == ( {'c' : {'d': 'e'}}, 3))
		self.assertTrue( dicttree.get(d, ['a'], False) == (d, 0))
		
	def test_dicttree_set(self):
		d = {}
		dicttree.set(d, ['a'], 'y'), dicttree.set(d, ['b', 'c', 'd'], 'x'), dicttree.set(d, ['b', 'e'], 'z')
		self.assertTrue( d == {'a': 'y', 'b': {'c': {'d': 'x'}, 'e': 'z'}})
		d = {}
		dicttree.set(d, ['a'], {2 : 3}), dicttree.set(d, ['a', 2], 4), dicttree.set(d, ['b'], ['foo', 'bar'])
		self.assertTrue( d == {'a': {2: 4}, 'b': ['foo', 'bar']})
		d = {}
		dicttree.set(d, ['a', 'b', 'c'], 'x'), dicttree.set(d, ['a'], 'y')
		self.assertTrue( d == {'a' : 'y'})
		#TODO this is test for get and set. move to tests
		d={"a":1}
		dicttree.set(d,["a","b","c"],1)
		self.assertTrue(d == {'a': {'b': {'c': 1}}})
		return True
