#!/usr/bin/env python
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

import datetime

def round9_10(n):
	i=int(n)
	if n-i>0.9:
		return i+1
	return i

def age(td):
	days=float(td.days)
	if days:
		years=round9_10(days/356)
		if years:
			return [years, years is 1 and "year" or "years"]
		months=round9_10(days/30)
		if months:
			return [months, months is 1 and "month" or "months"]
		weeks=round9_10(days/7)
		if weeks:
			return [weeks, weeks is 1 and "week" or "weeks"]
		days=int(days)
		return [days, days is 1 and "day" or "days"]
	seconds=float(td.seconds)
	if seconds:
		hours=round9_10(seconds/3600)
		if hours:
			return [hours, hours is 1 and "hour" or "hours"]
		minutes=round9_10(seconds/60)
		if minutes:
			return [minutes, minutes is 1 and "minute" or "minutes"]
		seconds=int(seconds)
		return [seconds, seconds is 1 and "second" or "seconds"]
	return [0,"now"]

def now():
	return datetime.datetime.now()
