#!/usr/bin/env python

from ACR.utils import json_compat
from pymongo.json_util import default
def serialize(acenv):
	if not json_compat:
		return "ERROR: JSON serializer not installed"
	#try:
	return json_compat.dumps(acenv.generations,default=default, indent=4)
	#except:
	#	raise Exception("simplejson module not installed. Can't output JSON.")
