#!/usr/bin/env python
from ACR.utils.xmlextras import tree2xml

name="ObjectML (Python ver)"
def serialize(env):
	xml=tree2xml(env.generations)
	xslt=""
	if env.output["XSLTFile"]:
		xslt="""<?xml-stylesheet type="text/xsl" href="http://%s/xslt/%s"?>\n"""%(env.domain,env.output["XSLTFile"])
	#TODO allow one-object output
	return """<?xml version="1.0" encoding="UTF-8"?>\n%s%s\n"""%(xslt,xml)

#TODO Generator
#def serialize(env):
#	xslt=""
#	if env.output["XSLTFile"]:
#		xslt="""<?xml-stylesheet type="text/xsl" href="http://%s/xslt/%s"?>\n"""%(env.domain,env.output["XSLTFile"])
#	yield """<?xml version="1.0" encoding="UTF-8"?>\n%s"""%xslt
#	for i in tree2xml(env.generations,True):
#		yield i
