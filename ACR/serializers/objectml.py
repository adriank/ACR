#!/usr/bin/env python
from ACR.utils.xmlextras import tree2xml

def serialize(env):
	xml=tree2xml(env.generations,True)
	xslt=""
	if env.output["xsltfile"]:
		xslt="""<?xml-stylesheet type="text/xsl" href="%sxslt/%s"?>\n"""%(env.domain,env.output["xsltfile"])
	#TODO allow one-object output
	return """<?xml version="1.0" encoding="UTF-8"?>\n%s%s\n"""%(xslt,xml)
