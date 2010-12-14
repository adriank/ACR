#!/usr/bin/env python
from distutils.core import setup
setup(
	name = 'acruntime',
	version = '0.3',
	description = 'Asyncode Runtime',
	author = 'Adrian Kalbarczyk',
	author_email = 'office@asyncode.com',
	url = 'http://www.asyncode.com/',
	packages = ['ACR', 'ACR.backends', 'ACR.cache', 'ACR.components',
	'ACR.core', 'ACR.db', 'ACR.plugins', 'ACR.serializers', 'ACR.session',
	'ACR.utils'],
	requires = ['libxml2', 'libxslt', 'psycopg2'],
)
