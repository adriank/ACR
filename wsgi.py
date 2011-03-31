#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("/root/acr/ACRA")
sys.path.append("/root/acr")
from ACR.backends.WSGIHandler import application
from ACR import acconfig
acconfig.appsDir="/var/ACF"