#!/usr/bin/python
# -*- coding: utf-8 -*-

# Asyncode Runtime - XML framework allowing developing internet
# applications without using programming languages.
# Copyright (C) 2008-2010  Adrian Kalbarczyk

# This program is free software: you can redistribute it and/or modify
# it under the terms of the version 3 of GNU General Public License as published by
# the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#@marcin: docstrings

import urllib,time,cgi
from ACR.utils.xmlextras import escapeQuotes,unescapeQuotes
from ACR import acconfig
from email.Utils import formatdate

#D=False

#SLOW!!!
def computePOST(env):
	post=None
	contentType=env['CONTENT_TYPE']
	if contentType.startswith("application/x-www-form-urlencoded"):
		POST=env['wsgi.input'].read()
		post=parseurlencoded(POST)
	elif contentType.startswith("multipart/form-data"):
		form=cgi.FieldStorage(env['wsgi.input'],environ=env)
		post={}
		for i in form.keys():
			if type(form[i]) is list:
				l=[]
				for item in form[i]:
					l.append(urllib.unquote_plus(item.value))
				post[i]=l
			elif form[i].filename is not None:
				post[i]={
					"filename":form[i].filename,
					"content":form[i].value
				}
			else:
				post[i]=form[i].value
	return post

def parseurlencoded(s):
	"""
	Parse url posts, from url string.
	input: url containing post inputs separated by '&' character, each one is name=val
	returns: dict {name1:val1, name2:val2, ..., name_n:val_n}
	"""
	#if D: log.info("Parsing POST data: %s",escapeQuotes(s))
	t=str(s).split("&")
	d={}
	for i in t:
		t2=i.split("=")
		d[t2[0]]=urllib.unquote_plus(t2[1])
	return d

def parseMultipart(f,tag):
	#if D: log.info("Parsing Multipart/form data (data in HTTP section of this Debug information), tag is %s",tag)
	import cgi
	#log.critical("This is not working! Fix needed.")
	raise str(cgi.FieldStorage(f).keys())
	ret=[]
	for ln in f:
		if ln[0]=='-' and ln[2:].strip()==tag:
			d={}
			for l in f:
				if len(l)<3 and len(l.strip())==0:
					break
				h=l.split(": ",1)
				if h[0]=="Content-Disposition":
				#example: Content-Disposition: form-data; name="file2"; filename="upload.html"
					params=h[1].split(";")
					for i in params:
						j=i.strip().split("=")
						if len(j)==2:
							j[1]=j[1].strip()
							d[j[0]]=j[1][1:len(j[1])-1]
				elif h[0]=="Content-Type":
					d[h[0]]=h[1].strip()
			ret.append(d)
	#WTF
	#raise str(ret)

def printHeaders(headers):
	"""
	Convert htttp headers from list to string.
	input: list containing http headers, each header is also list which length is 2.
	output: multi-line string, each line is a pair of words distanced by ':' delimeter
	"""
	#if D: log.debug("Printing headers")
	t=[]
	h=headers
	for i in h:
		t.append(i[0]+":"+i[1]+"\n")
	return "".join(t)

def getCookieDate(epoch_seconds=None):
	"""
	input: time.time()
	returns: 'Wdy, DD-Mon-YYYY HH:MM:SS GMT'.
	"""
	#if D: log.debug("getCookieDate")
	rfcdate = formatdate(epoch_seconds)
	return '%s-%s-%s GMT' % (rfcdate[:7], rfcdate[8:11], rfcdate[12:25])

def parseCookies(acenv,s):
	"""
	input: key=val;key=val
	returns: d={name:val}
	"""
	D = acenv.doDebug
	if D: acenv.debug("parseCookies '%s'",s)
	t=str(s).split(";")
	d={}
	for i in t:
		t2=i.split("=")
		t2[0]=t2[0].strip()
		if t2[0].startswith(acenv.prefix):
			#delete escapeQuotes
			d[t2[0]]=escapeQuotes(urllib.unquote(t2[1].replace("+"," ")))
	return d

def setCookie(acenv,cookie, test=False):
	"""
	Inserts a cookie to acconfig.request.headers.
	input: an Environment object's instance and dict.
	returns: if optional parameter test is set, returns headers.
					 otherwise, returns None
	"""
	D = acenv.doDebug
	if D: acenv.debug("Adding %s to output headers",cookie)
	s=acenv.prefix+cookie['name']+"="+cookie['value']
	if cookie.has_key("date"):
		date=cookie['date']
	else:
		date=time.time()+60*60*24*356 #one year from now
	if date is not None:
		s+="; expires="+getCookieDate(date)
	if cookie.has_key("path"):
		s+="; path="+cookie["path"]
	acenv.outputHeaders.append(("Set-Cookie",s))
	if D: acenv.info("Added Set-Cookie:%s",s)
