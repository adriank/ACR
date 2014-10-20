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

dbschema="asyncode"
SECRET_KEY="MySecret"
appDir=""
appsDir=""
debug=False

MIMEmapper={
	"text/html":"html5",
	"application/xml":"objectml",
	"text/xml":"objectml",
	"application/json":"json",
	"json":"json",
	"application/xhtml+xml":"objectml",
	"text/plain":"text",
	"html5":"html5",
	"html":"html5",
	"binary":"binary",
	"application/octet-stream":"binary"
}
