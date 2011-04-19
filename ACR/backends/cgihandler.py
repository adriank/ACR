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

import os, sys
import wsgiref
sys.path.append("ACR")
from ACR.backends.WSGIHandler import application
from ACR import acconfig

acconfig.appDir=os.getcwd()+"/project"
write=sys.stdout.write

def _start_response(status, headers, exc_info=None):
	if exc_info is not None:
		raise exc_info[0], exc_info[1], exc_info[2]
	write("Status: "+status+"\n")
	for i in headers:
		write(i[0]+": "+i[1]+"\n")
	write("\n")

env = dict(os.environ)
if not env.has_key("PATH_INFO"):
	env["PATH_INFO"]="/"
env["wsgi.input"] = sys.stdin
env["wsgi.errors"] = sys.stderr
env["wsgi.version"] = (1, 0)
env["wsgi.run_once"] = True
#env["wsgi.url_scheme"] = wsgiref.util.guess_scheme(env)
env["wsgi.multithread"] = False
env["wsgi.multiprocess"] = False
#print "Content-type: text/html;\n\n"
result=application(env, _start_response)
if result is not None:
	for data in result:
		write(data)
#for i in env:
	#sys.stdout.write(str(i)+": "+str(env[i])+"<br/>")
