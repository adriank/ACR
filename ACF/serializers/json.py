#!/usr/bin/env python

try:
	import cjson as json
except:
	try:
		import simplejson as json
	except:
		try:
			import json
		except:
			json=None

def serialize(structure,params):
	#if D: log.info("Generating JSON")
	if not json:
		return "ERROR: JSON serializer not found"
	try:
		return json.dumps(acenv.tree)
	except:
		raise Exception("simplejson module not installed. Can't output JSON.")
