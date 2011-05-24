#!/usr/bin/python
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

from ACR.utils.xmlextras import unescapeQuotes
from ACR.errors import Error
from ACR.utils import str2obj
import re

class Default(object):
	def __init__(self,value=None,default=None,config=None):
		if default:
			self.default=self.setDefault(default)
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
		D=acenv and acenv.doDebug
		if D:acenv.start("Type.get")
		# "" is valid so is not None is needed!
		if value is not None:
			if D: acenv.end("Type.get value was set, returning with: '%s'",value)
			return self._prepareValue(value)
		try:
			if D and self.value: acenv.debug("END Type.get with self.value: '%s'",self.value)
			return self.value
		except:
			if self.__dict__.has_key("default"):
				if D: acenv.end("Type.get with self.default: '%s'",self.default.execute(acenv))
				return self.default.execute(acenv)
			else:
				if D: acenv.end("Type.get with error ValueNotVaild")
				raise Error("NotValidValue", "Validation failed and no default value was set.")

	def reset(self):
		self._value=None

	def validate(self,value,config=None):
		return True

	def _prepareValue(self,value):
		return value

	def __repr__(self):
		return type(self).__name__+"Type(default="+str(self.__dict__.get("default","ErrorOnInvalid"))+")"

class XML(Default):
	pass

class Text(Default):
	def validate(self,value,config=None):
		if not type(value) is str:
			raise Error("NotString", "Should be string but is %s",type(value))
		return True

	def _prepareValue(self,value):
		return unescapeQuotes(value.strip())

class Number(Default):
	def validate(self,value,config=None):
		if not value.isdigit():
			raise Error("NotNumber", "Should be number, but is %s",value)
		return True

	def _prepareValue(self,value):
		return int(value)

class Boolean(Default):
	def validate(self,value,config=None):
		if type(str2obj(value)) in [str,unicode]:
			raise Error("NotNumber", "Should be number, but is %s",value)
		return True

	def _prepareValue(self,value):
		return str2obj(value)

class Email(Default):
	EMAIL_RE=re.compile("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$")
	def validate(self,value,config=None):
		if not type(value) is str:
			raise Error("NotString", "Should be string but is %s",type(value))
		# shortest is a@a.pl == 6 letters
		if not (len(value)>5 and self.EMAIL_RE.match(value)):
			raise Error("NotValidEmailAddress", "Suplied value is not a valid e-mail address")
		return True

class Empty(Default):
	def validate(self,value,config=None):
		if not type(value) is str:
			raise Error("NotString", "Should be string but is %s",type(value))
		if len(value) is 0:
			return True
		else:
			raise Error("NotEmptyString", "Should be an empty string")

class NonEmpty(Default):
	def validate(self,value,config=None):
		if not type(value) is str:
			raise Error("NotString", "Should be string but is %s",type(value))
		if len(value)>0:
			return True
		else:
			raise Error("EmptyString", "Should not be an empty string")

class HEXColor(Default):
	COLOR_RE=re.compile("^([a-f]|[A-F]|[0-9]){3}(([a-f]|[A-F]|[0-9]){3})$")
	def validate(self,value,config=None):
		if not type(value) is str:
			raise Error("ShouldBeString", "Should be string but is %s",type(value))
		if not (len(value) in [3,6] and self.COLOR_RE.match(value)):
			raise Error("NotValidHEXColor", "Should be valid HEX color (xxx or xxxxxx where x is 1-9 or a-f)")
		return True

#COMPLEX TYPES

class List(Default):
	RE_DELIMITER=re.compile("\s*,\s*")
	def validate(self,value,config=None):
		if not type(value) is str:
			raise Error("NotString", "Should be string but is %s",type(value))
		return True

	def _prepareValue(self,value):
		return RE_DELIMITER.split(value)

class CSV(List):
	RE_DELIMITER=re.compile("\s*,\s*")
	pass

# file type

class File(Default):
	def set(self,value):
		self.value=self._prepareValue(value)

	def validate(self,value,config=None):
		return True

	def _prepareValue(self,value):
		return value
