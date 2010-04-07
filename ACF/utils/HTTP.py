#!/usr/bin/python
# -*- coding: utf-8 -*-

# AsynCode Framework - XML framework allowing developing internet
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

import urllib,time,logging
from ACF.utils.xmlextras import escapeQuotes
from ACF import globals
from email.Utils import formatdate

log = logging.getLogger('ACF.util.HTTP')
D=logging.doLog

def parseURL(path):
	"""
	path is: /val/val/
	returns tuple:
	(viewName,viewData[])
	"""
	path=path.strip()
	if D: log.info("Parsing URL path section %s",path)
	if not len(path):
		if D: log.info("Path empty. Changing to default View")
		return ("default",None)
	t=path.split("/")
	if t[0].isspace() or len(t[0]) is 0:
		t=t[1:]
	if t[len(t)-1].isspace() or len(t[len(t)-1]) is 0:
		t=t[:len(t)-1]
	if len(t) is 0:
		return ("default",None)
	return (t[0],t[1:])

def parsePOST(s):
	"""
	returns:
	d={name:val}
	"""
	if D: log.info("Parsing POST data: %s",escapeQuotes(s))
	t=str(s).split("&")
	d={}
	for i in t:
		t2=i.split("=")
		d[t2[0]]=escapeQuotes(urllib.unquote_plus(t2[1]))
	return d

def parseMultipart(f,tag):
	if D: log.info("Parsing Multipart/form data (data in HTTP section of this Debug information), tag is %s",tag)
	import cgi
	log.critical("This is not working! Fix needed.")
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
	raise str(ret)

def printHeaders(headers):
	if D: log.debug("Printing headers")
	t=[]
	h=headers
	for i in h:
		t.append(i[0]+":"+i[1]+"\n")
	return "".join(t)

def getCookieDate(epoch_seconds=None):
	"""
	input time.time()
	returns 'Wdy, DD-Mon-YYYY HH:MM:SS GMT'.
	"""
	if D: log.debug("getCookieDate")
	rfcdate = formatdate(epoch_seconds)
	return '%s-%s-%s GMT' % (rfcdate[:7], rfcdate[8:11], rfcdate[12:25])

def parseCookies(acenv,s):
	"""
	input: key=val;key=val
	returns: d={name:val}
	"""
	if D: log.debug("Parsing cookies '%s'",s)
	t=str(s).split(";")
	d={}
	for i in t:
		t2=i.split("=")
		t2[0]=t2[0].strip()
		if t2[0].startswith(acenv.prefix):
			d[t2[0]]=escapeQuotes(urllib.unquote(t2[1].replace("+"," ")))
	return d

def setCookie(acenv,cookie):
	if D: log.debug("Adding %s to globals.request.headers",cookie)
	s=acenv.prefix+cookie['name']+"="+cookie['value']
	if cookie.has_key("date"):
		date=cookie['date']
	else:
		date=time.time()+60*60*24*356 #one year from now
	if date is not None:
		s+="; expires="+getCookieDate(date)
	if cookie.has_key("path"):
		s+="; path="+cookie["path"]
	log.info("Added Set-Cookie:%s",s)
	globals.request.headers.append(("Set-Cookie",s))
