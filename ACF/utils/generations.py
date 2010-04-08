#!/usr/bin/env python
import logging,re

RE_ATTR=re.compile("'([^']+)': '([^']*)',*")

class Object(dict):
	status="ok"
	error=""
	_value=None
	def __init__(self,value=None):
		self._value=value

	def __str__(self):
		if type(self._value) is str:
			return self._value
		return u'unprintable'

	def __repr__(self):
		return "'"+self.__str__()+"'"

class List(list):
	status="ok"
	error=""
	_value=None
	def __init__(self,value=[]):
		self._value=value

	def __str__(self):
		if type(self._value) is str:
			return self._value
		return u'unprintable'

	def __repr__(self):
		return "'"+self.__str__()+"'"
