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

#@marcin: functions docstrings

import re

EMAIL_RE=re.compile("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$")
COLOR_RE=re.compile("^([a-f]|[A-F]|[0-9]){3}(([a-f]|[A-F]|[0-9]){3})$")

def checkType(datatype, s):
	"""
	Checks data.
	input: type of data ['number' | 'text' | 'email' | 'password' | 'hexcolor' | 'csv'] and data which should be checked
	returns: True if checking was succesfull, otherwise False
	"""
	#log.debug("Type checking with type '%s' and value='%s'",datatype,s)
	stripped=s.strip()
	if datatype == "number":
		return stripped.isdigit()
	elif datatype == "empty":
		return len(stripped) is 0
	elif datatype == "text":
		return not len(stripped) is 0
	elif datatype == "email":
		if len(s)>5: # shortest is a@a.pl == 6 letters
			return EMAIL_RE.match(stripped)
		else:
			#log.info("E-mail has to few characters")
			return False
	elif datatype=="password":
		return len(s)>0
	elif datatype=="hexcolor":
		return COLOR_RE.match(stripped)
	elif datatype=="csv":
		return not (stripped.isspace() or len(stripped) is 0)
	#log.info("Type not valid. Assuming value is proper.")
	return True
