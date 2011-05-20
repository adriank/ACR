#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@marcin: tests for functions: escapeQuotes, str2obj, last, xml2tree, tree2xml, NS2Tuple

import unittest
from ACR.utils.xmlextras import *
import os

class Utils_xmlextras(unittest.TestCase):
	def test_escapeQuotes(self):
		self.assertTrue(escapeQuotes(' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~') ==  ' !&quot;#$%&amp;&apos;()*+,-./0123456789:;&lt;=&gt;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~')

#	def test_last(self):
#		self.assertTrue(last([1, 2, 3, -1]) == -1)
#		self.assertTrue(last(('doo', 'bi', 'doo', 'the')) == 'the')
#		self.assertTrue(last('abcdefx') == 'x')

	def test_xml2tree(self):
		self.assertTrue(xml2tree('./test/test1.xml') == ('messages', None, [('note', {'id': '501'}, [('to', None, ['Tove']), ('from', None, ['Jani']), ('heading', None, ['Reminder']), ('body', None, ["Don't forget me this weekend!"])]), ('note', {'id': '502'}, [('to', None, ['Jani']), ('from', None, ['Tove']), ('heading', None, ['Re: Reminder']), ('body', None, ['I will not'])])]))
		self.assertTrue(xml2tree('./test/test2.xml') == ('root', {'name': 'simple', 'dir': 'foo/bar'}, [('node', {'kind': 'int'}, [('value', None, ['2222']), ('out', {'where': 'std'}, [])])]))
		self.assertTrue(xml2tree('./test/test3.xml') == ('catalog', None, [('product', {'product_image': 'cardigan.jpg', 'description': 'Cardigan Sweater'}, [('catalog_item', {'gender': "Men"}, [('item_number', None, ['QWZ5671']), ('price', None, ['39.95']), ('size', {'description': 'Medium'}, [('color_swatch', {'image': 'red_cardigan.jpg'}, ['Red'])]), ('size', {'description': 'Large'}, [('color_swatch', {'image': 'red_cardigan.jpg'}, ['Red'])])])])]))

	def test_tree2xml(self):
		r = ('root', {'name': 'simple', 'dir': 'foo/bar'}, [('node', {'kind': 'int'}, [('value', None, ['2222']), ('out', {'where': 'std'}, [])])])
		xml = tree2xml(r)
		file = open('tmp', 'w')
		file.write(xml)
		file.close()
		self.assertTrue(xml2tree('tmp') == r)
		r = ('catalog', None, [('product', {'product_image': 'cardigan.jpg', 'description': 'Cardigan Sweater'}, [('catalog_item', {'gender': "Men"}, [('item_number', None, ['QWZ5671']), ('price', None, ['39.95']), ('size', {'description': 'Medium'}, [('color_swatch', {'image': 'red_cardigan.jpg'}, ['Red'])]), ('size', {'description': 'Large'}, [('color_swatch', {'image': 'red_cardigan.jpg'}, ['Red'])])])])])
		xml = tree2xml(r)
		file = open('tmp', 'w')
		file.write(xml)
		file.close()
		self.assertTrue(xml2tree('tmp') == r)
		r = ('root', {'name': 'simple', 'dir': 'foo/bar'}, [('node', {'kind': 'int'}, [('value', None, ['2222']), ('out', {'where': 'std'}, [])])])
		xml = tree2xml(r)
		file = open('tmp', 'w')
		file.write(xml)
		file.close()
		self.assertTrue(xml2tree('tmp') == r)
		os.remove('tmp')

	def test_NS2Tuple(self):
		self.assertTrue(NS2Tuple('xmlns:sthsthsth') == ('xmlns', 'sthsthsth'))
