#!/usr/bin/env python
import re

name="Text"
def serialize(env):
	def rec(node):
		nodetype=type(node)
		if type(node) is dict:
			for i in node.iteritems():
				rec(i[1])
		elif type(node) is list:
			for i in node:
				if type(i) in (dict,list):
					rec(i)
				elif type(i) in [str,unicode]:
					tab.append(i)
		elif type(node) in [str,unicode]:
			tab.append(node)

	D=env.doDebug
	tab=[]
	rec(env.generations["layout"])
	for i in range(len(tab)):
		if type(tab[i]) is unicode:
			tab[i]=tab[i].encode("utf-8")
	ret="".join(tab)
	ret=re.sub("<br.*/>|</p>|</h.*>","\n",ret)
	ret=re.sub("<[^>]*>","",ret)
	if D: env.debug("Returned: %s",ret)
	return ret
