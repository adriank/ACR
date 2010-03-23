#!/usr/bin/env python
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

class Request:
	def __init__(self,env):
		self.env=env
	def getPostData(self):
		if self.env['REQUEST_METHOD'].lower() is "post":
			return sys.stdin.read()
		else:
			return None

	def getViewName(self):
		try:
			t=env['PATH_INFO'].split("/")
			if t.__len__()>1:
				t2=t[2:]
			else:
				t2=[]
			sess=""
			return component.start(t2,post,sess)
		except KeyError:
			return None
