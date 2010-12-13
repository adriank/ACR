#!/usr/bin/python
# -*- coding: utf-8 -*-

# AsynCode Framework - XML framework allowing developing internet
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

from ACR.utils.xmlextras import unescapeQuotes
from ACR.utils.generations import Object,List
from ACR.errors import Error
import re

class Type(object):
	def __init__(self,value=None,default=None,config=None):
		if default:
			self.default=self.setDefault(default)
		else:
			self.default=None
		if value:
			self.set(value,config)

	def set(self,value,config=None):
		if not value:
			return
		value=value.strip()
		if self.validate(value,config):
			self.value=self._prepareValue(value)
		else:
			raise Error("ValueNotVaild")

	def setDefault(self,default):
		self.default=default

	def get(self,acenv=None,value=None):
		if value:
			return self._prepareValue(value)
		try:
			return self.value
		except:
			if self.default:
				return self.default.execute(acenv)
			else:
				raise Error("NotValidValue")

	def reset(self):
		self._value=None

	#def __repr__(self):
	#	return str(self._value)
	#
	#def __str__(self):
	#	return self.__repr__()

	def validate(self,value,config=None):
		return True

	def _prepareValue(self,value):
		return Object(value)

class XML(Type):
	pass

class Text(Type):
	def validate(self,value,config=None):
		if not type(value) is str:
			raise Error("NotString", "Should be string but is %s",type(value))
		return True

	def _prepareValue(self,value):
		return Object(unescapeQuotes(value.strip()))

class Number(Type):
	def validate(self,value,config=None):
		#if not type(value) is str:
		#	raise Error("ShouldBeString", "Should be string but is %s",type(value))
		if not value.isdigit():
			raise Error("NotNumber", "Should be number")
		return True

	def _prepareValue(self,value):
		return Object(int(value))

class Email(Type):
	EMAIL_RE=re.compile("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$")
	def validate(self,value,config=None):
		if not type(value) is str:
			raise Error("NotString", "Should be string but is %s",type(value))
		# shortest is a@a.pl == 6 letters
		if not (len(value)>5 and self.EMAIL_RE.match(value)):
			raise Error("NotValidEmailAddress", "Suplied value is not a valid e-mail address")
		return True

class Empty(Type):
	def validate(self,value,config=None):
		if not type(value) is str:
			raise Error("NotString", "Should be string but is %s",type(value))
		# shortest is a@a.pl == 6 letters
		if len(value) is 0:
			return True
		else:
			raise Error("NotEmptyString", "Should be a empty string")

class NonEmpty(Type):
	def validate(self,value,config=None):
		if not type(value) is str:
			raise Error("NotString", "Should be string but is %s",type(value))
		# shortest is a@a.pl == 6 letters
		if len(value)>0:
			#print value
			return True
		else:
			raise Error("EmptyString", "Should be a not empty string")

class HEXColor(Type):
	COLOR_RE=re.compile("^([a-f]|[A-F]|[0-9]){3}(([a-f]|[A-F]|[0-9]){3})$")
	def validate(self,value,config=None):
		if not type(value) is str:
			raise Error("ShouldBeString", "Should be string but is %s",type(value))
		if not (len(value) in [3,6] and self.COLOR_RE.match(value)):
			raise Error("NotValidHEXColor", "Should be valid HEX color (xxx or xxxxxx where x is 1-9 or a-f)")
		return True

#COMPLEX TYPES

class List(Type):
	RE_DELIMITER=re.compile("\s*,\s*")
	def validate(self,value,config=None):
		if not type(value) is str:
			raise Error("NotString", "Should be string but is %s",type(value))
		return True

	def _prepareValue(self,value):
		return List(map(lambda x: Object(x), RE_DELIMITER.split(value)))

class CSV(List):
	RE_DELIMITER=re.compile("\s*,\s*")
	pass
