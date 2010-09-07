#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Debugger(object):
	dbg=False
	_debugStr=None
	dbgfn=None
	level=40
	CRITICAL=50
	ERROR=40
	WARNING=30
	INFO=20
	DEBUG=10
	
	def __init__(self):
		self._debugStr=[]
		self.dbgfn = self.consolelog
	
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
		if len(s)>1:
			self._debugStr.append((lvl, s[0] % s[1:]))
			print lvl, s[0] % s[1:]
		else:
			self._debugStr.append((lvl, s[0]))
			print lvl, s[0]