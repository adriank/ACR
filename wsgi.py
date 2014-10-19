#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/ubuntu/ACR")
from ACR.backends.WSGIHandler import application
from ACR import acconfig
acconfig.appsDir="/var/sites"