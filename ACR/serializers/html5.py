#!/usr/bin/env python
from ACR.utils.xmlextras import tree2xml
from ACR.utils import json_compat
from pymongo.json_util import default

def serialize(env):
	env.output["format"]="text/html"
	html=tree2xml(env.generations["layout"])
	del env.generations["layout"]
	#del env.output["html"]
	html=html.replace("</head>","<script>var appData="+json_compat.dumps(env.generations,default=default)+"</script></head>")
	return """<!DOCTYPE html>\n%s\n"""%(html)
