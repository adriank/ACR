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

def age(date,lang="en"):
	td=now()-date
	days=float(td.days)
	if days:
		years=round9_10(days/356)
		if years:
			if lang=="pl":
				return (years, years is 1 and "rok" or years<5 and "lata" or "lat")
			else:
				return (years, years is 1 and "year" or "years")
		months=round9_10(days/30)
		if months:
			if lang=="pl":
				return (months, months is 1 and "miesiąc" or months<5 and "miesiące" or "miesięcy")
			else:
				return (months, months is 1 and "month" or "months")
		weeks=round9_10(days/7)
		if weeks:
			if lang=="pl":
				return (weeks, weeks is 1 and "tydzień" or "tygodnie")
			else:
				return (weeks, weeks is 1 and "week" or "weeks")
		days=int(days)
		if lang=="pl":
			return (days, days is 1 and "dzień" or "dni")
		else:
			return (days, days is 1 and "day" or "days")
	seconds=float(td.seconds)
	if seconds:
		hours=round9_10(seconds/3600)
		if hours:
			if lang=="pl":
				return (hours, hours is 1 and "godzina" or hours<5 and "godziny" or "godzin")
			else:
				return (hours, hours is 1 and "hour" or "hours")
		minutes=round9_10(seconds/60)
		if minutes:
			if lang=="pl":
				return (minutes, minutes%10 is 1 and "minuta" or 1<minutes%10<5 and "minuty" or "minut")
			else:
				return (minutes, minutes is 1 and "minute" or "minutes")
		seconds=int(seconds)
		if lang=="pl":
			return (seconds, seconds is 1 and "sekunda" or 1<seconds%10<5 and "sekundy" or "sekund")
		else:
			return (seconds, seconds is 1 and "second" or "seconds")
	return (0,"now")

def now():
	return datetime.datetime.now()
