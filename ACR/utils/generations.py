#!/usr/bin/env python

class Generation(object):
	status="ok"
	error=""
	_value=None
	def __init__(self,value=None):
		self._value=value

	def addAttrs(self,attrs):
		self.__dict__.update(attrs)

	def __repr__(self):
		return "'"+self.__str__()+"'"

class Object(Generation):
	_name="object"
	def __str__(self):
		if type(self._value) is str:
			return self._value
		return u'un#printable'

class List(Generation):
	_name="list"
	#def __init__(self,value=None):
	#	#checks if value is indeed a list (iterable, sequence)
	#	iter(value)
	#	self._value=value

	def __str__(self):
		if type(self._value) is str:
			return self._value
		return u'un#printable'
