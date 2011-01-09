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

from ACR import acconfig
import logging

log = logging.getLogger('ACR.session.file')

def create():
	log.info("Creating fake account")
	log.warning("Executing internal query")
	sql="insert into "+acconfig.dbschema+""".users DEFAULT VALUES;
	SELECT currval('"""+acconfig.dbschema+".users_id_seq') AS id"""
	id=acconfig.getDB().rawQuery(sql)[0]['id']
	log.info("Adding ID=%s, fake=True and lang=%s to session storage",id,acconfig.defaultLang)
	acconfig.session['ID']=id
	acconfig.session["fake"]=True
	acconfig.session['lang']=acconfig.defaultLang
