#!/usr/bin/env python
from ACF import globals

class ACTE(object):
	TEXTS_CACHE={}
	def __init__(self,config):
		self.textsDir=globals.appDir+"/texts"
		for i in config[2]:
			self.__dict__[i[0]]=i[2][0]
		#print self.__dict__

engine=ACTE
