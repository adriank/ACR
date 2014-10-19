#!/usr/bin/env python
from ACR.utils.xmlextras import tree2xml
from ACR.utils import json_compat
try:
	from pymongo.json_util import default
except:
	from bson.json_util import default

def serialize(env):
	env.output["format"]="text/html"
	try:
		html=tree2xml(env.generations["layout"])
		del env.generations["layout"]
	except:
		html="<html><head></head><body></body></html>"
	#del env.output["html"]
	try:
		html=html.replace("</head>","<script>var appData="+json_compat.dumps(env.generations,default=default)+"</script></head>")
	except:
		pass
	return """<!DOCTYPE html>\n%s\n"""%(html)
