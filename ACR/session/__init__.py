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

# highly modified Django code, relicensed under GPL

import os,sys,time,random,base64
from ACR import acconfig
from ACR.utils import HTTP
from datetime import datetime, timedelta
from ACR.utils.hashcompat import md5_constructor
import time
try:
	import cPickle as pickle
except ImportError:
	import pickle

if hasattr(random, 'SystemRandom'):
	randrange = random.SystemRandom().randrange
else:
	randrange = random.randrange
MAX_SESSION_KEY = 18446744073709551616L

#try changing object to dict
class Session(object):
	def __init__(self, acenv, ID=False):
		if self.D: acenv.info("START Session.__init__ with id=%s",ID)
		self.modified=False
		self.delCookie=False
		self.data={}
		self.env=acenv
		self.sessID=ID
		#print "sessID ",self.sessID
		if self.sessID:
			#print self.load
			self.load()
		else:
			self.create()

	def __contains__(self, key):
		return key in self.data

	def has_key(self, key):
		return key in self.data

	def __getitem__(self, key):
		return self.data[key]

	def __setitem__(self, key, value):
		self.data[key] = value
		self.modified = True

	def __delitem__(self, key):
		del self.data[key]
		self.modified = True

	def generateID(self, secret=acconfig.SECRET_KEY):
		"Returns session key that isn't being used."
		# The random module is seeded when this Apache child is created.
		# Use settings.SECRET_KEY as added salt.
		try:
			pid = os.getpid()
		except AttributeError:
			# No getpid() in Jython, for example
			pid = 1
		while 1:
			session_key = md5_constructor("%s%s%s%s" % (randrange(0, MAX_SESSION_KEY), pid, time.time(), secret)).hexdigest()
			if not self.exists(session_key):
				break
		return session_key

	def encode(self, session_dict):
		"Returns the given session dictionary pickled and encoded as a string."
		pickled = pickle.dumps(session_dict, pickle.HIGHEST_PROTOCOL)
		pickled_md5 = md5_constructor(pickled + acconfig.SECRET_KEY).hexdigest()
		return base64.encodestring(pickled + pickled_md5)

	def decode(self, session_data):
		encoded_data = base64.decodestring(session_data)
		pickled, tamper_check = encoded_data[:-32], encoded_data[-32:]
		if md5_constructor(pickled + acconfig.SECRET_KEY).hexdigest() != tamper_check:
			raise SuspiciousOperation("User tampered with session cookie.")
		try:
			return pickle.loads(pickled)
		# Unpickling can cause a variety of exceptions. If something happens,
		# just return an empty dictionary (an empty session).
		except:
			return {}

	def create(self):
		#print("executed, function with no parameters")
		self.sessID=self.generateID()
		HTTP.setCookie(self.env,{"name":"SESS", "value":self.sessID, "path":"/"})

	def deleteCookie(self):
		#log.info("Deleting session cookie")
		t=time.time()-10000
		#log.debug("Session cookie deleted by setting date to %s",t)
		HTTP.setCookie(self.env,{"name":"SESS", "value":"", "date":t})
		return

	def save(self, must_create=False):
		"""
		Saves the session data. If 'must_create' is True, a new session object
		is created (otherwise a CreateError exception is raised). Otherwise,
		save() can update an existing object with the same key.
		"""
		raise NotImplementedError

	def delete(self, session_key=None):
		"""
		Deletes the session data under this key. If the key is None, the
		current session key value is used.
		"""
		raise NotImplementedError

	def load(self):
		"""
		Loads the session data and returns a dictionary.
		"""
		raise NotImplementedError

	def exists(self, session_key):
		"""
		Returns True if the given session_key already exists.
		"""
		raise NotImplementedError
