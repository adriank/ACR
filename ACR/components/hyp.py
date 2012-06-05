#!/usr/bin/python
from hyphen import hyphenator
from hyphen.dictools import *
from xml.sax import make_parser
from xml.sax.handler import ContentHandler 
lang="pl_PL"
if not is_installed(lang): 
	install(lang)
h_pl = hyphenator('pl_PL')

class XMLHyphenator(ContentHandler):
	def __init__ (self):
		self.isPointsElement, self.isReboundsElement = 0, 0
		self.outputXML=[]
	def startElement(self, name, attrs):
		self.outputXML.append("<"+name)
		for i in attrs.keys():
			self.outputXML.append(" "+i+"=\""+attrs.get(i,"")+"\"")
		self.outputXML.append(">")
		return
	def endElement(self, name):
		self.outputXML.append("</"+name+">")
		return
	def characters (self, ch):
		t=ch.split(" ")
		for i in t:
			s=i
			if i.__len__()>5:
				if i[len(i)-1]==",":
					i=h_pl.inserted(i.replace(",",""))+","
				else:
					i=h_pl.inserted(i)
			self.outputXML.append(i.replace("=","&shy;")+" ")
		return
parser = make_parser()
x=XMLHyphenator()
parser.setContentHandler(x)
parser.parse(open('haze.html'))
#print h_pl.inserted(i)
print "".join(x.outputXML)
