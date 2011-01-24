#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Asyncode Runtime - XML framework allowing developing internet
# applications without using programming languages.
# Copyright (C) 2008-2010  Adrian Kalbarczyk

# This program is free software: you can redistribute it and/or modify
# it under the terms of the version 3 of GNU General Public License as published by
# the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
HINTS:
 - object atributes are fastest (even faster than dict!)
 - objects do not keep the attributes order, neither do dict
"""
class Generation(object):
	status="ok"
	error=""
	HTML_ATTR_PATTERN=' %s="%s"'
	ATTR_PATTERN="<%s>%s</%s>"
	def __init__(self, value=None):
		self.set(value)

	def __getattr__(self, name):
		return Generation.__dict__[name]

	def set(self,value):
		self._value=value

	def __repr__(self):
		return "'"+self.__str__()+"'"

class Object(Generation):
	"""
		Object stores its attributes in the list of 2-value tuples:
		[
			(name,value),
			(name,value)
		]
		This structure provides a ordering of attributes and can store more than one attribute with the same name.
	"""
	_name="object"
	START_TAG="<object"
	END_TAG="</object>"
	#RE_ATTR=re.compile("'([^']+)': '([^']*)',*")
	def add(self,name,value):
		self._value.append((name,value))

	def addAttrs(self,attrs):
		self._value.extend(attrs)

	def __getattr__(self, name):
		try:
			return Object.__dict__[name]
		except:
			return super(Object,self).__getattr__(name)

	def __getitem__(self,name,default=None):
		try:
			return filter(lambda x: x[0]==name,self._value)[0][1]
		except:
			return default

	def toXML(self):
		"""
		returns tuple where:
		l[0] - string with '%s'
		l[1] - list of values
		"""
		s=[self.START_TAG]
		values=[]
		attrs=self.__dict__
		for i in attrs.iteritems():
			if not i[0][0] is '_':
				s.append(self.HTML_ATTR_PATTERN%(i[0],"%s"))
				values.append(i[1])
		if not attrs["_value"]:
			s.append("/>")
		else:
			s.append(">")
			if type(self._value) is not list:
				s.append("%s")
				values.append(self._value)
			else:
				for i in self._value:
					s.append(self.ATTR_PATTERN%(i[0],"%s",i[0]))
					values.append(i[1])
			s.append(self.END_TAG)
		return ("".join(s),values)

	def __str__(self):
		if type(self._value) is str:
			return self._value
		return "'"+self._name+"'"


class List(Generation):
	_name="list"
	START_TAG="<list"
	END_TAG="</list>"
	def toXML(self):
		#XXX dont know what to do with name
		#if len(self._value) is 1:
		#	return self._value[0].toXML()
		s=[self.START_TAG]
		values=[]
		attrs=self.__dict__
		for i in attrs.iteritems():
			if not i[0][0] is '_':
				s.append(self.HTML_ATTR_PATTERN%(i[0],"%s"))
				values.append(i[1])
		s.append(">")
		for i in self._value:
			pattern,vals=i.toXML()
			s.append(pattern)
			values.extend(vals)
		s.append(self.END_TAG)
		return ("".join(s),values)

	def __getattr__(self, name):
		try:
			return List.__dict__[name]
		except:
			return super(List,self).__getattr__(name)

	def __str__(self):
		if type(self._value) is str:
			return self._value
		return "'"+self._name+"'"
