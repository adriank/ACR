#!/usr/bin/env python
from ACF.errors import Error

try:
	from cjson import *
	#TODO unify cjson API with simplejson/json
except:
	try:
		from simplejson import *
	except:
		try:
			from json import *
		except:
			raise Error("JSONNotFound")
