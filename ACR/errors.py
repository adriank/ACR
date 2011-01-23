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

class AppNotFound(Exception):
	MESG="""Application config not found at %s!
You should 
	"""
	def __init__(self,path):
		super(AppNotFound, self).__init__(self.MESG%path)

class Err(Exception):
	def __init__(self, name, msg=""):
		self.error=msg
		self.name=name

	def __str__(self):
		s=""+self.name
		if len(self.error)>0:
			s+=": "+self.error
		return s

	def get(self):
		return ("object",{"type":"error","name":self.name},[self.error])

class AbstractClass(Exception):
	def __init__(self, error=""):
		self.error=self.msg="You are trying to acces abstract class"

#framework error
class Error(Err):
	pass

#user application error
class AppError(Err):
	pass

#terminate other actions
class TerminatingError(Err):
	pass

class ViewNotFound(Exception):
	pass
