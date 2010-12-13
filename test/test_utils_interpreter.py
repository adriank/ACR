#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@marcin: tests for interpreter and helper functions

from ACR.utils.interpreter import *
from random import randint, choice
import sys, unittest, os

# change a global settings - depth of recursion
sys.setrecursionlimit(20000)

# --------------------- helpers -------------------------------------

# helper functions for creating correctness tests
def generate():
	file = open('testFile', 'w')
	#print 'Testing parser. Enter a program or \'q\' for exit.'
	while 1:
		s = raw_input("program: ")
		if s == 'q':
			break
		ans = make_tree(s)
		#print "Answer: %s. Correct [y|n] ?" % str(ans),
		yesno = raw_input()
		if yesno == 'y':
			file.write('self.assertTrue(make_tree("%s") == %s)\n' % (s,ans))
	file.close()
	
# generate efficiency arithm test
def generateEff_arith(n):
	s = str(randint(0,100))
	for i in range(0,n-1):
		r = randint(0,3)
		if r == 0:
			s += '+'
		elif r == 1:
			s += '*'
		elif r == 2:
			s += '/'
		else:
			s += '-'
		s += str(randint(0,100))
	return s

# generate random variable with or without storage
def generateVar(storage=True):
	s = ""
	if storage: # with storage
		s += choice(['ss', 'rs', 'session', 'request']) + '::'
	for i in range(0, randint(1,5)):
		s += choice('abcde') + '.'
	return s[0:-1] # without last character (dot)

# generate efficiency variable test
def generateEff_var(n):
	s = generateVar()
	for i in range(0, n-1):
		s += '+' + generateVar() # simply adding variables
	return s
	
def generateFileTest(s, path):
	file = open(path, 'w')
	file.write(s + '\n')
	file.write(str(make_tree(s)))
	file.close()

# efficiency tests, reads data from file, which consists of two lines:
# first is data in, and second data out (expected out)
def test_efficiency(id):
	def new_test():
		file = open ('./test/test' + str(id), 'r')
		s1 = file.readline().rstrip()
		s2 = file.readline().rstrip()
		assert (str(make_tree(s1)) == s2)
		file.close()
		return True
	new_test.__name__ = 'test_efficiency' + str(id)
	return new_test

# --------------------------------------------------------------

class Utils_interpreter(unittest.TestCase):
	# corectness tests		
	# associativity, addition, subtraction, multiplication, division, name literals
	def test_add(self):
		self.assertTrue((make_tree("2+3") == ('+',2,3)))
		self.assertTrue((make_tree("2+(3+4)") == ('+', 2, ('+', 3, 4))))
		self.assertTrue((make_tree("2+3+4") == make_tree("(2+3)+4")))
	
	def test_sub(self):
		self.assertTrue(make_tree("2-3") == ('-', 2, 3))
		self.assertTrue(make_tree("2-(3-4)") == ('-', 2, ('-', 3, 4)))
		self.assertTrue(make_tree("(2-3)-4") == ('-', ('-', 2, 3), 4))

	def test_mul(self):
		self.assertTrue(make_tree("2*3*5*6") == ('*', ('*', ('*', 2, 3), 5), 6))
		self.assertTrue(make_tree("(2*3)*4") == ('*', ('*', 2, 3), 4))
		self.assertTrue(make_tree("2*(3*4)") == ('*', 2, ('*', 3, 4)))

	def test_div(self):	
		self.assertTrue(make_tree("1/2/3") == ('/', ('/', 1, 2), 3))
		self.assertTrue(make_tree("1/(2/3)/4") == ('/', ('/', 1, ('/', 2, 3)), 4))

	def test_arithm_group(self):	
		self.assertTrue((make_tree("2-3+4+5-7") == ('-', ('+', ('+', ('-', 2, 3), 4), 5), 7)))
		self.assertTrue((make_tree("33*2/5-2") == ('-', ('/', ('*', 33, 2), 5), 2)))
		self.assertTrue((make_tree("33-4*5+2/6") == ('+', ('-', 33, ('*', 4, 5)), ('/', 2, 6))))
		self.assertTrue((make_tree("2//3//4//5") == ('//', ('//', ('//', 2, 3), 4), 5)))
	
	def test_arithm_bracktes(self):
		self.assertTrue((make_tree("(33-4)*5+2/6") == ('+', ('*', ('-', 33, 4), 5), ('/', 2, 6))))
		self.assertTrue((make_tree("2/3/(4/5)*6") == ('*', ('/', ('/', 2, 3), ('/', 4, 5)), 6)))
		self.assertTrue((make_tree("((2+4))+6") == ('+', ('+', 2, 4), 6)))
	
	def test_or(self):
		self.assertTrue((make_tree("1 or 2 or 3") == ('or', 1, ('or', 2, 3))))
	
	def test_and(self):
		self.assertTrue((make_tree("1 and (2 and 3)") == ('and', 1, ('and', 2, 3))))
	
	def test_not(self):
		self.assertTrue(make_tree("not 222") == ('not', 222))
		self.assertTrue((make_tree("not not not 7") == ('not', ('not', ('not', 7)))))

	def test_and_or_not(self):
		self.assertTrue((make_tree("(1 and 2) or 3") == ('or', ('and', 1, 2), 3)))
		self.assertTrue((make_tree("not 1 and 2") == ('and', ('not', 1), 2)))
		self.assertTrue((make_tree("not (1 and 2)") == ('not', ('and', 1, 2))))
		self.assertTrue((make_tree("(not 1) and 2") == ('and', ('not', 1), 2)))
	
	def test_is(self):
		self.assertTrue(make_tree("2 is 3") == ('is', 2, 3))

	def test_isnot(self):
		self.assertTrue(make_tree("3 is not 6") == ('is not', 3, 6))
		
	def test_notin(self):
		self.assertTrue(make_tree("4 not in 6") == ('not in', 4, 6))
		self.assertTrue(make_tree("1 not in 5 not in 00") == ('not in', ('not in', 1, 5), 0))

	def test_is_isnot_notin_arithm(self):
		self.assertTrue((make_tree("23 is not 56 or 25 is 57") == ('or', ('is not', 23, 56), ('is', 25, 57))))
		self.assertTrue((make_tree("2 is 3 is not (not 5)") == ('is not', ('is', 2, 3), ('not', 5))))
		self.assertTrue((make_tree("1 + 2 or 3 / (not 4)") == ('or', ('+', 1, 2), ('/', 3, ('not', 4)))))
		self.assertTrue((make_tree("4     and 5       - 1") == ('and', 4, ('-', 5, 1))))
		self.assertTrue((make_tree("2+3/4-6*7 or 10 is not 11 and 14") == ('or', ('-', ('+', 2, ('/', 3, 4)), ('*', 6, 7)), ('and', ('is not', 10, 11), 14))))
	
	def test_prefix(self):
		self.assertTrue((make_tree("~2 + +3") == ('+', ('~', 2), ('+', 3))))
		self.assertTrue((make_tree("++3") == ('+', ('+', 3))))
		self.assertTrue((make_tree("-+-3") == ('-', ('+', ('-', 3)))))
	
	def test_greater_less(self):
		self.assertTrue((make_tree("2 < 3 < 4 < 5") == ('<', ('<', ('<', 2, 3), 4), 5)))
		self.assertTrue((make_tree("1 <= (2 <= 3)") == ('<=', 1, ('<=', 2, 3))))
	
	def test_greater_less_prefixs_or(self):
		self.assertTrue((make_tree("2 >= 1 or +1") == ('or', ('>=', 2, 1), ('+', 1))))
		self.assertTrue((make_tree("+1 <= ~2 > -3") == ('>', ('<=', ('+', 1), ('~', 2)), ('-', 3))))
	
	def test_tuple(self):
		self.assertTrue(make_tree("(1, 2, 3)") == ('(', [1, 2, 3]))

	def test_list(self):
		self.assertTrue((make_tree("[1, 2, 3]") == ('[', [1, 2, 3])))
		
	def test_symbol_dot(self):
		self.assertTrue(make_tree("a.b") == ('.', ('name', 'a'), ('name', 'b')))
		# TODO test "a.b.c",  invalid!
	
	def test_operator_sqarebrackets(self):
		self.assertTrue(make_tree("2[3]") == ('[', 2, 3))
		self.assertTrue(make_tree("2[3][4][5]") == ('[', ('[', ('[', 2, 3), 4), 5))

	def test_operator_sqarebrackets_symbol_dot_add_sub_lessequal(self):
		self.assertTrue((make_tree("object.variable + 2 - list[0]") == ('-', ('+', ('.', ('name', 'object'), ('name', 'variable')), 2), ('[', ('name', 'list'), 0))))
		self.assertTrue((make_tree("list[6].object[1] <= 1111111") == ('<=', ('[', ('.', ('[', ('name', 'list'), 6), ('name', 'object')), 1), 1111111))	)
		
	def test_const_prefixs_isnot_and_or(self):
		self.assertTrue((make_tree("None") == None))
		self.assertTrue((make_tree("True or False and None") == ('or', True, ('and', False, None))))
		self.assertTrue((make_tree("~true") == ('~', ('name', 'true'))))
		self.assertTrue((make_tree("~True is not False") == ('is not', ('~', True), False)))
	
	def test_storage_var(self):
		self.assertTrue(make_tree("ss::var") == ('(variable)', 'ss', 'var'))
		self.assertTrue(make_tree("session::var.foo") == ('(variable)', 'session', 'var.foo'))
		self.assertTrue(make_tree("request::var.s") == ('(variable)', 'request', 'var.s'))
		self.assertTrue(make_tree("rs::a.b.c.d.e") == ('(variable)', 'rs', 'a.b.c.d.e'))

	
	# tests invalid expressions
	def test_invalidExpression(self):
		try: make_tree("not 1 not 2")
		except Exception: pass
		else: return False
		try: make_tree("{$sesion::a.b.c}")
		except Exception: pass
		else: return False
		try: make_tree("{$session:a.b.c}")
		except Exception: pass
		else: return False
		return True

testcase1=unittest.FunctionTestCase(test_efficiency(1))
testcase2=unittest.FunctionTestCase(test_efficiency(2))
testcase3=unittest.TestLoader().loadTestsFromTestCase(Utils_interpreter)

utils_interpreter=unittest.TestSuite([testcase1, testcase2, testcase3])
