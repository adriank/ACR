#!/usr/bin/env python
from distutils.core import setup
setup(
	name = 'ACR',
	version = '0.1',
	description = 'AsynCode Runtime',
	author = 'Adrian Kalbarczyk',
	author_email = 'biuro@asyncode.com',
	url = 'http://www.asyncode.com/',
	packages = ['ACR', 'ACR.backends', 'ACR.components',
	'ACR.core', 'ACR.db', 'ACR.plugins', 'ACR.serializers', 'ACR.session',
	'ACR.utils', 'ACTE'],
	requires = ['libxml2', 'libxslt', 'pg', 'psycopg2'],
#	package_dir = {'ACTE' : 'ACTE'},
#	package_data = {'ACTE' : ['*']},
)
