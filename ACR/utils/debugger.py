#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect

class Debugger(object):
	dbg=None
	_debugStr=None
	dbgfn=None
	level=60
	CUT_AFTER=100
	# error levels
	CRITICAL=50
	ERROR=40
	WARNING=30
	INFO=START=END=20
	DEBUG=10
	doDebug=False

	def __init__(self, app):
		self._debugStr=[]
		self.dbgfn=self.consolelog
		self.dbgMap={
			"debug":self.DEBUG,
			"info":self.INFO,
			"start":self.START,
			"end":self.END,
			"warning":self.WARNING,
			"error":self.ERROR,
			"critical":self.CRITICAL
		}
		try:
			if app.dbg["enabled"]:
				self.doDebug=True
				self.level=self.dbgMap[app.dbg["level"].lower()]
				if app.dbg.has_key("cutAfter"):
					self.CUT_AFTER=app.dbg["cutAfter"]
				self.info("All strings will be cuted to %s chatacters. You can change this behavior by setting cutAfter attribute of debuger in config file. 0 to switch it off."%self.CUT_AFTER)
		except (KeyError, TypeError):
			pass

	def debug(self, *s):
		if self.dbgfn and self.level <= self.DEBUG:
			self.dbgfn("DEBUG", s)

	def info(self, *s):
		if self.dbgfn and self.level <= self.INFO:
			self.dbgfn("INFO", s)

	def start(self, *s):
		if self.dbgfn and self.level <= self.INFO:
			self.dbgfn("START", s)

	def end(self, *s):
		if self.dbgfn and self.level <= self.INFO:
			self.dbgfn("END", s)

	def warning(self, *s):
		if self.dbgfn and self.level <= self.WARNING:
			self.dbgfn("WARNING", s)

	def error(self, *s):
		if self.dbgfn and self.level <= self.ERROR:
			self.dbgfn("ERROR", s)

	def	critical(self, *s):
		if self.dbgfn and self.level<= self.CRITICAL:
			self.dbgfn("CRITICAL", s)

	def lineno(self):
			"""Returns the current line number in our program."""
			return inspect.currentframe().f_back.f_back.f_back.f_lineno

	def consolelog(self, lvl, s):
		def color(c,s):
			return '\033[%sm%s\033[0m' % (c,s)

		colors={
			"DEBUG":33,
			"INFO":36
		}

		def f(x):
			if type(x) is unicode:
				x=x.encode("utf8")
			if self.CUT_AFTER and type(x) is dict:
				s=[]
				for i in x.iteritems():
					s.append("'%s': %s"%(i[0],repr(i[1])[:self.CUT_AFTER]))
					if len(s[-1])>self.CUT_AFTER:
						s.append("...")
				return "{\n\t"+",\n\t".join(s)+"\n}"
			s=str(x).replace("\n","").replace("\t","")
			if self.CUT_AFTER and len(s)>self.CUT_AFTER:
				return s[:self.CUT_AFTER]+"..."
			else:
				return x

		if len(s)>1:
			v=tuple(map(f ,s[1:]))
			self._debugStr.append((lvl, s[0] %v))
			print lvl + "@" + str(self.lineno()) + " " + color(colors.get(lvl, 0), s[0] % v)
		else:
			self._debugStr.append((lvl, s[0]))
			print lvl + "@" + str(self.lineno()) + " " + color(colors.get(lvl, 0), f(s[0]))
