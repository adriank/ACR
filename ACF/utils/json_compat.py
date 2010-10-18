#!/usr/bin/env python
from ACF.errors import Error

try:
	from cjson import *
	#TODO unify cjson API with simplejson/json
except:
	try:
		import simplejson as json
	except:
		try:
			import json
		except:
			raise Error("JSONNotFound")

def loads(s):
	def tostr(dct):
		d={}
		for key in dct.keys():
			if type(dct[key]) is unicode:
				v=str(dct[key])
			else:
				v=dct[key]
			d[str(key)]=v
		return d

	return json.loads(s, object_hook=tostr)

load=json.load
dumps=json.dumps
dump=json.dump