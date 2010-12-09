#!/usr/bin/env python
from ACR.utils.xmlextras import tree2xml

def serialize(env):
	fragments=[]
	for i in env.generations.values():
		fragments.append(tree2xml(i))
	xslt=""
	if env.output["xsltfile"]:
		xslt="""<?xml-stylesheet type="text/xsl" href="%sxslt/%s"?>\n"""%(env.domain,env.output["xsltfile"])
	#TODO allow one-object output
	return """<?xml version="1.0" encoding="UTF-8"?>\n%s<list>%s</list>\n"""%(xslt,"".join(fragments))