#!/usr/bin/env python
from ACF.utils.xmlextras import tree2xml

def serialize(self,structure):
	#if D: log.info("Generating XML")
	return """<?xml version="1.0" encoding="UTF-8"?>\n%s"""%(tree2xml(structure))
