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

# highly modified Django code, relicensed under GPL

import errno,os,tempfile
from ACF import globals
from ACF.session import Session
from ACF.errors import Error

#log = logging.getLogger('ACF.session.file')

class FileSession(Session):
	def __init__(self, acenv, id=None):
		#log.info("Created FileSession object with id=%s",id)
		#TODO check if dir exists and raise error when not
		self.sessDir=acenv.app.sessionDir
		#log.info("Session directory is set to %s",self.sessDir)
		super(FileSession, self).__init__(acenv,id)

	def exists(self,id):
		return False

	def _key_to_file(self):
		return os.path.join(self.sessDir, self.id)

	def save(self):
		#log.info("Saving session")
		if not self.modified:
			#log.info("Session is not modified")
			return
		#log.info("Session is modified")
		if self.delCookie:
			self.deleteCookie()
		session_data = self.data
		session_file_name = self._key_to_file()
		try:
			# Make sure the file exists.  If it does not already exist, an
			# empty placeholder file is created.
			flags = os.O_WRONLY | os.O_CREAT | getattr(os, 'O_BINARY', 0)
#			flags |= os.O_EXCL
			fd = os.open(session_file_name, flags)
			os.close(fd)
		except OSError, e:
			#log.error("CreateError: session file couldn't be created")
			raise CreateError
		dir, prefix = os.path.split(session_file_name)
		try:
			output_file_fd, output_file_name = tempfile.mkstemp(dir=dir,
				prefix=prefix + '_out_')
			renamed = False
			try:
				try:
					os.write(output_file_fd, self.encode(session_data))
				finally:
					os.close(output_file_fd)
				os.rename(output_file_name, session_file_name)
				renamed = True
			finally:
				if not renamed:
					os.unlink(output_file_name)
		except (OSError, IOError, EOFError),e:
			#log.error("%s, %s",e["name"],e["message"])
			pass

	def load(self):
		#log.info("Loading session from file.")
		#log.debug("Executing - function w/o parameters")
		session_data = {}
		try:
			session_file = open(self._key_to_file(), "rb")
			try:
				file_data = session_file.read()
				# Don't fail if there is no data in the session file.
				# We may have opened the empty placeholder file.
				if file_data:
					try:
						session_data = self.decode(file_data)
					except (EOFError, SuspiciousOperation):
						#log.error("File corrupted. Creating empty session.")
						raise e
			finally:
				session_file.close()
		except IOError,e:
			#log.warning("Session file not found.")
			raise e
		#log.info("Session data set to %s",session_data)
		self.data=session_data

	def delete(self):
		#log.info("Deleting session")
		try:
			os.unlink(self._key_to_file())
		except OSError:
			pass
		self.delCookie=True
