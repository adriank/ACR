#!/usr/bin/env python
from ACF.utils.xmlextras import tree2xml
from ACF.errors import Error
#TODO change it to AC CRITICAL error.
try:
	import libxml2
	import libxslt
except:
	raise Error("libxsltError","libxslt not installed")

def transform(xml,xslt):
	try:
		doc=libxml2.parseDoc(xml)
	except Exception,e:
		return "XML parsing Error."
	try:
		#TODO implement checking for change of *ALL* xslt files
		XSLTCache=libxslt.parseStylesheetDoc(libxml2.parseFile(xslt))
#		raise str(dir(globals.XSLTCache))
	except Exception,e:
		return "XSLT parsing Error."
	r=XSLTCache.applyStylesheet(doc, None)
	ret=r.serialize()
	doc.freeDoc()
	r.freeDoc()
	return ret

def serialize(env):
	fragments=[]
	for i in env.generations.values():
		fragments.append(tree2xml(i))
	xslt=""
	if env.output["xsltfile"]:
		xslt="""\n<?xml-stylesheet type="text/xsl" href="/xslt/%s"?>\n"""%(env.output["xsltfile"])
	#TODO allow one-object output
	return transform("""<?xml version="1.0" encoding="UTF-8"?><list>%s</list>\n"""%("".join(fragments)),env.output["xsltfile"])
