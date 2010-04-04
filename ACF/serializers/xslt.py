#!/usr/bin/env python
from ACF.utils.xmlextras import tree2xml

def serialize(structure,params):
	xsl="""<?xml-stylesheet type="text/xsl" href="/xslt/%s"?>\n"""%params["xsltfile"]
	xml="""<?xml version="1.0" encoding="UTF-8"?>\n%s%s"""%(xsl,tree2xml(structure))
	return xml
