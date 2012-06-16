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

#TODO its 31 minuta, should be 31 minut - probably done

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
	if seconds is not None:
		hours=round9_10(seconds/3600)
		if hours:
			if lang=="pl":
				return (hours, hours is 1 and "godzina" or hours<5 and "godziny" or "godzin")
			else:
				return (hours, hours is 1 and "hour" or "hours")
		minutes=round9_10(seconds/60)
		if minutes:
			if lang=="pl":
				return (minutes, minutes is 1 and "minuta" or minutes%10 is 1 and "minuta" or 1<minutes%10<5 and "minuty" or "minut")
			else:
				return (minutes, minutes is 1 and "minute" or "minutes")
		seconds=int(seconds)
		if lang=="pl":
			return (seconds, seconds is 1 and "sekunda" or 1<seconds%10<5 and "sekundy" or "sekund")
		else:
			return (seconds, seconds is 1 and "second" or "seconds")
	#return (0,"seconds")

now=datetime.datetime.now

def date(d):
	if d:
		d=d[0]
		t=type(d)
		if t is datetime.datetime:
			return datetime.date(d.year,d.month,d.day)
		if t in (tuple,list):
			return datetime.date(*d)
	return datetime.date.today()

def time(d):
	if not d or not d[0]:
		d=now()
	else:
		d=d[0]
		t=type(d)
		if t in (tuple,list):
			return datetime.time(*d)
	return datetime.time(d.hour,d.minute,d.second,d.microsecond)

def dateTime(arg):
	"""
	d may be:
	 - datetime()
	 - [y,m,d,h,m,ms]
	 - [date(),time()]
	 - [[y,m,d],[h,m,s,ms]]
	 and permutations of above
	"""
	l=len(arg)
	if l is 1:
		dt=arg[0]
		typed=type(dt)
		if typed is datetime.datetime:
			return dt
		if typed in (tuple,list) and len(dt) in [5,7]:
			return datetime.datetime(*dt)
	if l is 2:
		date=time=None
		if type(arg[0]) is datetime.date:
			d=arg[0]
			date=[d.year,d.month,d.day]
		if type(arg[0]) in (tuple,list):
			date=arg[0]
		if type(arg[1]) is datetime.time:
			t=arg[1]
			time=[t.hour,t.minute,t.second,t.microsecond]
		if type(arg[1]) in (tuple,list):
			time=arg[1]
		return datetime.datetime(*date+time)
