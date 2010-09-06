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

import re

EMAIL_RE=re.compile("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$")
#COLOR_RE=re.compile("^?([a-f]|[A-F]|[0-9]){3}(([a-f]|[A-F]|[0-9]){3})?$")

def checkType(datatype, s):
	#log.debug("Type checking with type '%s' and value='%s'",datatype,s)
	if datatype == "number":
		return s.strip().isdigit()
	elif datatype == "text":
		return not len(s.strip()) is 0
	elif datatype == "email":
		if len(s)>5: # shortest is a@a.pl == 6 letters
			return EMAIL_RE.match(s)
		else:
			log.info("E-mail has to few characters")
			return False
	elif datatype=="password":
		return len(s)>0
	elif datatype=="hexcolor":
		return COLOR_RE.match(s)
	elif datatype=="csv":
		return not (s.isspace() or len(s) is 0)
	log.info("Type not valid. Assuming value is proper.")
	return True
