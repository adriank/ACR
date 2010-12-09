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

from ACR.backends.WSGIHandler import application

def _start_response(status, headers, exc_info=None):
  if exc_info is not None:
    raise exc_info[0], exc_info[1], exc_info[2]
  print "Status: %s" % status
  for name, val in headers:
    print "%s: %s" % (name, val)
  print
  return sys.stdout.write

env = dict(os.environ)
env["wsgi.input"] = sys.stdin
env["wsgi.errors"] = sys.stderr
env["wsgi.version"] = (1, 0)
env["wsgi.run_once"] = True
env["wsgi.url_scheme"] = wsgiref.util.guess_scheme(env)
env["wsgi.multithread"] = False
env["wsgi.multiprocess"] = False
result = application(env, _start_response)
if result is not None:
	for data in result:
		sys.stdout.write(data)