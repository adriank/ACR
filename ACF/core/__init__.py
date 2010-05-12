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

from ACF.core.view import View
from ACF.utils.xmlextras import tpath

class Environment(object):
	"""
	The Environment object is a structure of data which is passed through whole application. Each function manipulates its contents and passes it to next function. After application execution is done, Environment instance is deleted. This way framework is thread-safe, because there can be many Environment instances in the system at the particular moment.
	The prototype for Environment instances properties is the Application instance.
	"""
	viewName=""
	appName=""
	inputs=None
	#debug=None
	cookies=None
	outputHeaders=None
	session=None
	app=None
	sessionStorage=None
	requestStorage=None
	appStorage=None
	lang=""
	URL=""
	UA=""
	IP=""
	output=None
	prefix="ACF_"
	doRedirect=False
	redirect=False
	tree=None
	_debugStr=None
	_debug=None

	def __init__(self,app):
		self.generations={}
		self.mime=[]
		#populate with app defaults; the class attributes are not in __dict__!
		self.__dict__.update(filter(lambda t: t[0] in Environment.__dict__, list(app.__dict__.iteritems())))
		self.requestStorage={}
		self.outputHeaders=[]
		self.cookies={}
		self.inputs=[]
		self.posts={}
		#self.debug=app.debug.copy()
		self.app=app
		self._debugStr=[]
		self._debug=10

	def setLang(self,lang):
		if not lang:
			return
		if self.cookies.has_key(self.prefix+"pagelang"):
			self.lang=self.cookies[self.prefix+"pagelang"]
		elif lang:
			l=lang.split(",")[0].split("-")[0]
			if l in self.app.langs:
				self.lang=l

	def __str__(self):
		s=["Environment("]
		d=dict(Environment.__dict__.items()+self.__dict__.items())
		for i in d:
			if i[0]!="_":
				s.append(str(i)+": "+str(d[i]))
		s.append(")")
		return ", ".join(s)

	def dbg(self, *s):
		if self._debug <= 10:
			self.dbgfn("DEBUG", s)
	
	def info(self, *s):
		if self._debug <= 20:
			self.dbgfn("INFO", s)
	
	def warning(self, *s):
		if self._debug <= 30:
			self.dbgfn("WARNING", s)

	def error(self, *s):
		if self._debug <= 40:
			self.dbgfn("ERROR", s)
		
	def	critical(self, *s):
		if self._debug <= 50:
			self.dbgfn("CRITICAL", s)

	def dbgfn(self, msg, s):
		if len(s)>1:
			self._debugStr.append((msg, s[0] % s[1:]))
			print msg+": ", s[0] % s[1:]
		else:
			self._debugStr.append((msg, s[0]))
			print msg+": ",s[0]
