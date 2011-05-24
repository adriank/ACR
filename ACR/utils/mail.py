#!/usr/bin/env python
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

import os
from subprocess import *
SENDMAIL = "/usr/sbin/sendmail"

def send(headers, content):
	m=[]
	if not headers.has_key("Content-Type"):
		headers["Content-Type"]="text/plain; charset=UTF-8"
	for i in headers:
		k=i.strip()
		v=headers[i]
		if type(k) is unicode:
			k=k.encode("utf8")
		if type(v) is unicode:
			v=v.encode("utf8")
		m.append(k+": "+v+"\n")
	m.append("\n")
	if type(content) is unicode:
		content=content.encode("utf8")
	m.append(content)
	try:
		p=Popen([SENDMAIL,"-t"], bufsize=2024, stdin=PIPE)
	except OSError:
		raise Exception("%s failed with error code %s"%(SENDMAIL,res))
	for i in m:
		p.stdin.write(i)
	p.stdin.close()
	p=None
