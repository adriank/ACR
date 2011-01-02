#!/usr/bin/env python
from ACR.utils.xmlextras import tree2xml
from ACR.errors import Error
import os
#TODO change it to AC CRITICAL error.
try:
	import libxml2
	import libxslt
except:
	raise Error("libxsltError","libxslt not installed")

XSLTCache={}

def transform(xml,xslt):
	try:
		doc=libxml2.parseDoc(xml)
	except Exception,e:
		return "XML parsing Error."
	if not XSLTCache.has_key(xslt):
		try:
			#TODO implement checking for change of *ALL* xslt files
			XSLTCache[xslt]=libxslt.parseStylesheetFile(xslt)
	#		raise str(dir(acconfig.XSLTCache))
		except Exception,e:
			return "XSLT parsing Error."
	r=XSLTCache[xslt].applyStylesheet(doc, None)
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
		xslt="""<?xml-stylesheet type="text/xsl" href="/xslt/%s"?>\n"""%(env.output["xsltfile"])
	#TODO allow one-object output
	return transform("""<?xml version="1.0" encoding="UTF-8"?><list>%s</list>\n"""%("".join(fragments)),os.path.join(env.app.appDir,"static/xslt",env.output["xsltfile"]))
