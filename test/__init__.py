#!/usr/bin/env python
# -*- coding: utf-8 -*-
#unit tests for ACF functions

from test_utils___init__ import Utils_init
from test_utils_interpreter import utils_interpreter
from test_utils_dicttree import Utils_dicttree
from test_utils_xmlextras import Utils_xmlextras
from test_utils_http import Utils_http
from test_utils_checktype import Utils_checktype

import unittest

def doTests():
	print 'Started ACF testing.\n'

	utils_init = unittest.TestLoader().loadTestsFromTestCase(Utils_init)
	utils_dicttree = unittest.TestLoader().loadTestsFromTestCase(Utils_dicttree)
	utils_xmlextras = unittest.TestLoader().loadTestsFromTestCase(Utils_xmlextras)
	utils_http = unittest.TestLoader().loadTestsFromTestCase(Utils_http)
	utils_checktype = unittest.TestLoader().loadTestsFromTestCase(Utils_checktype)

	print 'utils/init.py'	
	unittest.TextTestRunner(verbosity = 2).run(utils_init)
	print '\nutils/dicttree.py'
	unittest.TextTestRunner(verbosity = 2).run(utils_dicttree)
	print '\nutils/interpreter.py'
	unittest.TextTestRunner(verbosity = 2).run(utils_interpreter)
	print '\nutils/xmlextras.py'
	unittest.TextTestRunner(verbosity = 2).run(utils_xmlextras)
	print '\nutils/HTTP.py'
	unittest.TextTestRunner(verbosity = 2).run(utils_http)
	print '\nutils/checktype.py'
	unittest.TextTestRunner(verbosity = 2).run(utils_checktype)
	
	print 'Ended ACF testing.'