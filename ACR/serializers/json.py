#!/usr/bin/env python

from ACR.utils import json_compat
from pymongo.json_util import default
from bson.objectid import ObjectId

def hook(dct):
	r=default(dct)
	return r.values()[0]

name="JSON"
def serialize(acenv):
	if not json_compat:
		return "ERROR: JSON serializer not installed"
	#try:
	return json_compat.dumps(acenv.generations,default=hook)
	#except:
	#	raise Exception("simplejson module not installed. Can't output JSON.")
