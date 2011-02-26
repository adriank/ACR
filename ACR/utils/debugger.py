#!/usr/bin/env python
# -*- coding: utf-8 -*-

# move dbgMap outside

class Debugger(object):
	dbg=None
	_debugStr=None
	dbgfn=None
	level=60
	CUT_AFTER=12011
	CRITICAL=50
	ERROR=40
	WARNING=30
	INFO=20
	DEBUG=10

	def __init__(self, app):
		self._debugStr=[]
		self.dbgfn=self.consolelog
		self.dbgMap={
			"debug":self.DEBUG,
			"info":self.INFO,
			"warning":self.WARNING,
			"error":self.ERROR,
			"critical":self.CRITICAL}
		try:
			if app.dbg["enabled"]:
				self.doDebug=True
				self.level = self.dbgMap[app.dbg["level"].lower()]
		except (KeyError, TypeError):
			print 'Cannot read debug settings from app config.'

	def debug(self, *s):
		if self.dbgfn and self.level <= self.DEBUG:
			self.dbgfn("DEBUG", s)

	def info(self, *s):
		if self.dbgfn and self.level <= self.INFO:
			self.dbgfn("INFO", s)

	def warning(self, *s):
		if self.dbgfn and self.level <= self.WARNING:
			self.dbgfn("WARNING", s)

	def error(self, *s):
		if self.dbgfn and self.level <= self.ERROR:
			self.dbgfn("ERROR", s)

	def	critical(self, *s):
		if self.dbgfn and self.level<= self.CRITICAL:
			self.dbgfn("CRITICAL", s)

	def consolelog(self, lvl, s):
		def f(x):
			if type(x) is unicode:
				x=x.encode("utf8")
			s=str(x).replace("\n","").replace("\t","")
			if len(s)>self.CUT_AFTER:
				return s[:self.CUT_AFTER]+"..."
			else:
				return x
		if len(s)>1:
			v=tuple(map(f ,s[1:]))
			self._debugStr.append((lvl, s[0] %v))
			print lvl, s[0] % v
		else:
			self._debugStr.append((lvl, s[0]))
			print lvl, f(s[0])
