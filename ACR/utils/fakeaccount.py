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

from ACR import globals
import logging

log = logging.getLogger('ACR.session.file')

def create():
	log.info("Creating fake account")
	log.warning("Executing internal query")
	sql="insert into "+globals.dbschema+""".users DEFAULT VALUES;
	SELECT currval('"""+globals.dbschema+".users_id_seq') AS id"""
	id=globals.getDB().rawQuery(sql)[0]['id']
	log.info("Adding ID=%s, fake=True and lang=%s to session storage",id,globals.defaultLang)
	globals.session['ID']=id
	globals.session["fake"]=True
	globals.session['lang']=globals.defaultLang
