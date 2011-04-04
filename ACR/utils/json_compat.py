#!/usr/bin/env python
from ACR.errors import Error

try:
	import cjson3
	print "cjson"
	def dumps(s,default):
		print s
		return cjson.encode(s)
	#TODO unify cjson API with simplejson/json
except:
	try:
		import json
	except:
		try:
			import simplejson as json
		except:
			raise Error("JSONNotFound")

#def loads(s,object_hook=None):
	#def tostr(dct):
	#	d={}
	#	for key in dct.keys():
	#		if type(dct[key]) is unicode:
	#			v=str(dct[key])
	#		else:
	#			v=dct[key]
	#		d[str(key)]=v
	#	return d

	#return json.loads(s, object_hook=object_hook)
	loads=json.loads
	load=json.load
	def dumps(s,default):
		json.dumps(s,default=default, separators=(',',':'))
	dump=json.dump
