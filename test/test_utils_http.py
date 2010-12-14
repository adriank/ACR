#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@marcin: tests for functions: parsePOST, #printHeaders, setCookie, parseCookies

import unittest
from ACR.utils.HTTP import *

class myAcenv:
	def __init__(self):
		self.prefix = "ACR_"
		self.dbg = None
		self.outputHeaders = []
		self.doDebug = False

class Utils_http(unittest.TestCase):
	def test_parseurlencoded(self):
		self.assertTrue(parseurlencoded('act[0]=0&word[0]=unescape&lang[0]=&act[1]=1&word[1]=escape&lang[1]=') == {'lang[0]': '', 'lang[1]': '', 'act[0]': '0', 'act[1]': '1', 'word[0]': 'unescape', 'word[1]': 'escape'})
		self.assertTrue(parseurlencoded('a=2+2') == {'a': '2 2'})
		self.assertTrue(parseurlencoded('a=foo/bar&b=g[0]&c=foo.bar') == {'a': 'foo/bar', 'c': 'foo.bar', 'b': 'g[0]'})
		self.assertEqual(parseurlencoded('a=foo/bar&b=g[0]&c=foo.bar&d=\'mar\''), {'a': 'foo/bar', 'c': 'foo.bar', 'b': 'g[0]', 'd': '\'mar\''})

	def test_printHeaders(self):
		self.assertTrue( printHeaders([
['Server', 'Apache'],
['X-Backend-Server', 'pm-app-amo11'],
['Vary' ,'Accept-Encoding'],
['Content-Type', 'text/xml'],
['X-amo-darklaunch', 'z'],
['Content-Encoding', 'gzip'],
['Date', 'Thu, 09 Sep 2010 10:29:41 GMT'],
['Keep-Alive', 'timeout=5, max=999'],
['Via', 'Moz-Cache-zlb03'],
['X-Frame-Options', 'DENY']]) ==
"""Server:Apache
X-Backend-Server:pm-app-amo11
Vary:Accept-Encoding
Content-Type:text/xml
X-amo-darklaunch:z
Content-Encoding:gzip
Date:Thu, 09 Sep 2010 10:29:41 GMT
Keep-Alive:timeout=5, max=999
Via:Moz-Cache-zlb03
X-Frame-Options:DENY
""")
		
	def test_getCookieDate(self):
		self.assertTrue(getCookieDate(757696555) == 'Tue, 04-Jan-1994 15:15:55 GMT')
		self.assertTrue(getCookieDate(188412992) == 'Sun, 21-Dec-1975 16:56:32 GMT')
		self.assertTrue(getCookieDate(137092263) == 'Mon, 06-May-1974 17:11:03 GMT')
		self.assertTrue(getCookieDate(779207391) == 'Sat, 10-Sep-1994 14:29:51 GMT')
		self.assertTrue(getCookieDate(628354017) == 'Wed, 29-Nov-1989 14:46:57 GMT')
		self.assertTrue(getCookieDate(530627402) == 'Sat, 25-Oct-1986 12:30:02 GMT')
		self.assertTrue(getCookieDate(968950914) == 'Thu, 14-Sep-2000 17:01:54 GMT')
		self.assertTrue(getCookieDate(672534531) == 'Wed, 24-Apr-1991 23:08:51 GMT')
		self.assertTrue(getCookieDate(192744939) == 'Mon, 09-Feb-1976 20:15:39 GMT')
		self.assertTrue(getCookieDate(518390305) == 'Thu, 05-Jun-1986 21:18:25 GMT')

	def test_setCookie(self):
		env = myAcenv()
		setCookie(env, {'name': 'foo', 'value': 'bar'}, True)
		ret = env.outputHeaders
		self.assertTrue(ret[0][0] == 'Set-Cookie')
		t = ret[0][1].split(';')
		t2 = t[0].split('=')
		self.assertTrue(t2[0] == 'ACR_foo', t2[1] == 'bar')

		date = 1129281102
		env = myAcenv()
		setCookie(env, {'name': 'foo', 'value': 'bar', 'date' : date}, True)
		ret = env.outputHeaders
		t = ret[0][1].split(';')
		t2 = t[1].split('=')
		self.assertTrue(getCookieDate(date) == t2[1])
	
	def test_parseCookies(self):
		self.assertTrue(parseCookies(myAcenv(), 'ACR_a =b;c=d') == {'ACR_a': 'b'})
		self.assertTrue(parseCookies(myAcenv(), 'ACR_a ="b"') == {'ACR_a': '&quot;b&quot;'})
		self.assertTrue(parseCookies(myAcenv(), 'ACR_a =b + 2') == {'ACR_a': 'b   2'})
