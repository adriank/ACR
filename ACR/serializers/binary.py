#!/usr/bin/env python

def serialize(acenv):
	acenv.output["format"]="application/octet-stream"
	File=acenv.generations["binary"]
	acenv.outputHeaders.append(("Content-Disposition","attachment; filename=\""+File["fileName"]+'";'))
	return File["content"]
