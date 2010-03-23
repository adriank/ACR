#!/usr/bin/env python
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

from ACF import globals
from ACF.errors import *
from ACF.utils import replaceVars, evaluate
import logging

log = logging.getLogger('ACF.util.conditionChecker')

def interpretInternal(code):
	t=code.split()
	Not=False
	variable=""
	for i in t:
		if i.lower()=="not":
			log.debug("Found 'Not'")
			Not=True
		else:
			log.debug("Found variable")
			variable=i
	ret=evaluate(variable)
	if Not:
		ret=not ret
	#casts any to bool
	return not not ret

def check(condition, data=None):
	"""
	condition:
	{
		"lang":"",
		"errorString":"",
		"code":[node-set]
	}
	"""
	log.info("Executed with condition=%s and data=%s",condition,data)
	result=False
	if condition["lang"] is None:
		log.info("'lang' is not set. Using XML predefined actions.")
		for i in condition["code"]:
			if i[0].lower()=="user":
				if i[1].has_key("role") and globals.session is not None and globals.session.has_key('role') and i[1]["role"]==globals.session['role']:
					result=True
	elif condition["lang"].lower()=="internal":
		log.info("'lang' is internal")
		result=interpretInternal(condition["code"][0])
		log.info("Result is %s",result)
	elif condition["lang"].lower()=="python":
		log.info("'lang' is Python")
		if globals.session is not None:
			ss=globals.session.data
		else:
			ss=None
		locals={"session":ss}
		if data:
			for i in data:
				locals[i]=data[i]
		log.debug("Locals are %s",locals)
		try:
			log.debug("Executed with %s",condition["code"][0])
			result=eval(condition["code"][0],{},locals)
		except Exception,e:
			raise Error("PythonCodeError",str(e))

	elif condition["lang"].lower() == "sql":
		log.info("'lang' is SQL")
		db=globals.getDB()
		if data is not None:
			for i in data:
				if i[0:1]!="__":
					data[i]=db.escapeString(data[i])
		sql=replaceVars(condition['code'][0])
		log.info("replaceVars returned '%s'",condition['code'])
		#rawQuery returns OrderedDict so it must be values()
		result=db.rawQuery(sql,dictionary=False)[0][0]
		log.debug("Result is %s",result)
		if result=="f":
			result=False
		elif result=="t":
			result=True

	if result is True:
		return True
	elif result is False:
		raise Error("ConditionNotFullfiled")
	else:
		raise Error("ConditionError","Condition should return True or False and is: "+ result)

def parse(n):
	if n[1]:
		attrs=n[1]
	else:
		attrs={}
	lang=None
	if attrs.has_key("lang"):
		lang=attrs["lang"].strip().lower()
	return {
		"lang":lang,
		"errorCode":attrs.get("errorCode","ConditionNotFullfiled"),
		"code":n[2],
		"terminate":attrs.get("terminate",False),
		"showError":attrs.get("showError",True)
	}
