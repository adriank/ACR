#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ACF.utils.objecttree import *
from ACF.utils.tester import Tester

# unit test for functions: getObject, set

def test_getObject():
	d = {'x': {'y': 'z', 'a' : {'b': {'c' : {'d': 'e'}}}}, 'w': 't', 'r' : {'o' : 'l', 'g' : {'q': 's'}} }
	assert getObject(d, ['x', 'y'], False) == ('z', 2)
	assert getObject(d, 'x.a.b.c.d'.split('.'), False) == ('e', 5)
	assert getObject(d, 'x.a.b.c.d'.split('.')) == 'e'
	assert getObject(d, ['w'], False) == ('t', 1)
	assert getObject(d, 'r.o'.split('.'), False) == ('l', 2)
	assert getObject(d, 'r.g.q'.split('.'), False) == ('s', 3)
	assert not getObject(d, 'x.y.z'.split('.'))
	assert not getObject(d, 'x.b'.split('.'))
	assert getObject(d, ['r', 'g']) ==  {'q': 's'}
	assert getObject(d, ['x', 'a', 'b'], False) == ( {'c' : {'d': 'e'}}, 3)
	assert getObject(d, ['a'], False) == (d, 0)
	return True

def test_setObject():
	d = {}
	setObject(d, ['a'], 'y'), setObject(d, ['b', 'c', 'd'], 'x'), setObject(d, ['b', 'e'], 'z')
	assert d == {'a': 'y', 'b': {'c': {'d': 'x'}, 'e': 'z'}}
	d = {}
	setObject(d, ['a'], {2 : 3}), setObject(d, ['a', 2], 4), setObject(d, ['b'], ['foo', 'bar'])
	assert d == {'a': {2: 4}, 'b': ['foo', 'bar']}
	d = {}
	setObject(d, ['a', 'b', 'c'], 'x'), setObject(d, ['a'], 'y')
	assert d == {'a' : 'y'}
	assert not setObject(d, ['a', 'b'] , 'x')
	return True

def doTests():
	tester = Tester("utils.objecttree")
	tester.addTest(test_getObject).addTest(test_setObject)
	tester.run()