#!/usr/bin/env python

"""
HINTS:
 - object atributes are fastest (even faster than dict!)
 - objects do not keep the attributes order, neither do dict
"""
class Generation(object):
	status="ok"
	error=""
	def __init__(self,value=None):
		self.set(value)

	def set(self,value):
		self._value=value

	def __repr__(self):
		return "'"+self.__str__()+"'"

class Object(Generation):
	"""
		Object stores its attributes in the list of 2-value tuples:
		[
			(name,value),
			(name,value)
		]
		This structure provides a ordering of attributes and can store more than one attribute with the same name.
	"""
	_name="object"
	START_TAG="<object"
	END_TAG="</object>"
	HTML_ATTR_PATTERN=' %s="%s"'
	ATTR_PATTERN="<%s>%s</%s>"
	#RE_ATTR=re.compile("'([^']+)': '([^']*)',*")
	def add(self,name,value):
		self._value.append((name,value))

	def addAttrs(self,attrs):
		self._value.extend(attrs)

	def get(self,name):
		return filter(lambda x: x[0]==name,self,_value)

	def toXML(self):
		"""
		returns tuple where:
		l[0] - string with '%s'
		l[1] - list of values
		"""
		s=[self.START_TAG]
		values=[]
		attrs=self.__dict__
		for i in attrs.iteritems():
			if not i[0][0] is '_':
				s.append(self.HTML_ATTR_PATTERN%(i[0],"%s"))
				values.append(i[1])
		if not attrs["_value"]:
			s.append("/>")
		else:
			s.append(">")
			if type(self._value) is not list:
				return ("%s",(self._value,))
			for i in self._value:
				s.append(self.ATTR_PATTERN%(i[0],"%s",i[0]))
				values.append(i[1])
			s.append(self.END_TAG)
		return ("".join(s),values)

	def __str__(self):
		if type(self._value) is str:
			return self._value
		return u'un#printable'

class List(Generation):
	_name="list"
	START_TAG="<list>"
	END_TAG="</list>"
	def toXML(self):
		#XXX dont know what to do with name
		#if len(self._value) is 1:
		#	return self._value[0].toXML()
		s=[START_TAG]
		values=[]
		for i in self._value:
			pattern,vals=i.toXML()
			s.append(pattern)
			values.extend(vals)
		s.append(END_TAG)
		return ("".join(),values)

	def __str__(self):
		if type(self._value) is str:
			return self._value
		return u'un#printable'
