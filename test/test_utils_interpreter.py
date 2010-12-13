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
	file.write(str(make_tree(s).tree))
	file.close()

# efficiency tests, reads data from file, which consists of two lines:
# first is data in, and second data out (expected out)
def test_efficiency(id):
	def new_test():
		file = open ('./test/test' + str(id), 'r')
		s1 = file.readline().rstrip()
		s2 = file.readline().rstrip()
		assert (str(make_tree(s1).tree) == s2)
		file.close()
		return True
	new_test.__name__ = 'test_efficiency' + str(id)
	return new_test

# --------------------------------------------------------------

class Utils_interpreter(unittest.TestCase):
	# corectness tests		
	# associativity, addition, subtraction, multiplication, division, name literals
	def test_add(self):
		self.assertEqual(make_tree("2+3").tree, ('+',2,3))
		self.assertEqual(make_tree("2+(3+4)").tree, ('+', 2, ('+', 3, 4)))
		self.assertEqual(make_tree("2+3+4").tree, make_tree("(2+3)+4").tree)
	
	def test_sub(self):
		self.assertEqual(make_tree("2-3").tree, ('-', 2, 3))
		self.assertEqual(make_tree("2-(3-4)").tree, ('-', 2, ('-', 3, 4)))
		self.assertEqual(make_tree("(2-3)-4").tree, ('-', ('-', 2, 3), 4))

	def test_mul(self):
		self.assertEqual(make_tree("2*3*5*6").tree, ('*', ('*', ('*', 2, 3), 5), 6))
		self.assertEqual(make_tree("(2*3)*4").tree, ('*', ('*', 2, 3), 4))
		self.assertEqual(make_tree("2*(3*4)").tree, ('*', 2, ('*', 3, 4)))

	def test_div(self):	
		self.assertEqual(make_tree("1/2/3").tree, ('/', ('/', 1, 2), 3))
		self.assertEqual(make_tree("1/(2/3)/4").tree, ('/', ('/', 1, ('/', 2, 3)), 4))

	def test_arithm_group(self):	
		self.assertEqual(make_tree("2-3+4+5-7").tree, ('-', ('+', ('+', ('-', 2, 3), 4), 5), 7))
		self.assertEqual(make_tree("33*2/5-2").tree, ('-', ('/', ('*', 33, 2), 5), 2))
		self.assertEqual(make_tree("33-4*5+2/6").tree, ('+', ('-', 33, ('*', 4, 5)), ('/', 2, 6)))
		self.assertEqual(make_tree("2//3//4//5").tree, ('//', ('//', ('//', 2, 3), 4), 5))
	
	def test_arithm_bracktes(self):
		self.assertEqual(make_tree("(33-4)*5+2/6").tree, ('+', ('*', ('-', 33, 4), 5), ('/', 2, 6)))
		self.assertEqual(make_tree("2/3/(4/5)*6").tree, ('*', ('/', ('/', 2, 3), ('/', 4, 5)), 6))
		self.assertEqual(make_tree("((2+4))+6").tree, ('+', ('+', 2, 4), 6))
	
	def test_or(self):
		self.assertEqual(make_tree("1 or 2 or 3").tree, ('or', 1, ('or', 2, 3)))
	
	def test_and(self):
		self.assertEqual(make_tree("1 and (2 and 3)").tree, ('and', 1, ('and', 2, 3)))
	
	def test_not(self):
		self.assertEqual(make_tree("not 222").tree, ('not', 222))
		self.assertEqual(make_tree("not not not 7").tree, ('not', ('not', ('not', 7))))

	def test_and_or_not(self):
		self.assertEqual(make_tree("(1 and 2) or 3").tree, ('or', ('and', 1, 2), 3))
		self.assertEqual(make_tree("not 1 and 2").tree, ('and', ('not', 1), 2))
		self.assertEqual(make_tree("not (1 and 2)").tree, ('not', ('and', 1, 2)))
		self.assertEqual(make_tree("(not 1) and 2").tree, ('and', ('not', 1), 2))
	
	def test_is(self):
		self.assertEqual(make_tree("2 is 3").tree, ('is', 2, 3))

	def test_isnot(self):
		self.assertEqual(make_tree("3 is not 6").tree, ('is not', 3, 6))
		
	def test_notin(self):
		self.assertEqual(make_tree("4 not in 6").tree, ('not in', 4, 6))
		self.assertEqual(make_tree("1 not in 5 not in 00").tree, ('not in', ('not in', 1, 5), 0))

	def test_is_isnot_notin_arithm(self):
		self.assertEqual(make_tree("23 is not 56 or 25 is 57").tree, ('or', ('is not', 23, 56), ('is', 25, 57)))
		self.assertEqual(make_tree("2 is 3 is not (not 5)").tree, ('is not', ('is', 2, 3), ('not', 5)))
		self.assertEqual(make_tree("1 + 2 or 3 / (not 4)").tree, ('or', ('+', 1, 2), ('/', 3, ('not', 4))))
		self.assertEqual(make_tree("4     and 5       - 1").tree, ('and', 4, ('-', 5, 1)))
		self.assertEqual(make_tree("2+3/4-6*7 or 10 is not 11 and 14").tree, ('or', ('-', ('+', 2, ('/', 3, 4)), ('*', 6, 7)), ('and', ('is not', 10, 11), 14)))
	
	def test_prefix(self):
		self.assertEqual(make_tree("~2 + +3").tree, ('+', ('~', 2), ('+', 3)))
		self.assertEqual(make_tree("++3").tree, ('+', ('+', 3)))
		self.assertEqual(make_tree("-+-3").tree, ('-', ('+', ('-', 3))))
	
	def test_greater_less(self):
		self.assertEqual(make_tree("2 < 3 < 4 < 5").tree, ('<', ('<', ('<', 2, 3), 4), 5))
		self.assertEqual(make_tree("1 <= (2 <= 3)").tree, ('<=', 1, ('<=', 2, 3)))
	
	def test_greater_less_prefixs_or(self):
		self.assertEqual(make_tree("2 >= 1 or +1").tree, ('or', ('>=', 2, 1), ('+', 1)))
		self.assertEqual(make_tree("+1 <= ~2 > -3").tree, ('>', ('<=', ('+', 1), ('~', 2)), ('-', 3)))
	
	def test_tuple(self):
		self.assertEqual(make_tree("(1, 2, 3)").tree, ('(', [1, 2, 3]))

	def test_list(self):
		self.assertEqual(make_tree("[1, 2, 3]").tree, ('[', [1, 2, 3]))
		
	def test_symbol_dot(self):
		self.assertEqual(make_tree("a.b").tree, ('.', ('name', 'a'), ('name', 'b')))
		# TODO test "a.b.c",  invalid!
	
	def test_operator_sqarebrackets(self):
		self.assertEqual(make_tree("2[3]").tree, ('[', 2, 3))
		self.assertEqual(make_tree("2[3][4][5]").tree, ('[', ('[', ('[', 2, 3), 4), 5))

	def test_operator_sqarebrackets_symbol_dot_add_sub_lessequal(self):
		self.assertEqual(make_tree("object.variable + 2 - list[0]").tree, ('-', ('+', ('.', ('name', 'object'), ('name', 'variable')), 2), ('[', ('name', 'list'), 0)))
		self.assertEqual(make_tree("list[6].object[1] <= 1111111").tree, ('<=', ('[', ('.', ('[', ('name', 'list'), 6), ('name', 'object')), 1), 1111111))
		
	def test_const_prefixs_isnot_and_or(self):
		self.assertEqual(make_tree("None").tree, None)
		self.assertEqual(make_tree("True or False and None").tree, ('or', True, ('and', False, None)))
		self.assertEqual(make_tree("~true").tree, ('~', True))
		self.assertEqual(make_tree("~True is not False").tree, ('is not', ('~', True), False))
	
	def test_storage_var(self):
		self.assertEqual(make_tree("ss::var").tree, ('(variable)', 'ss', 'var'))
		self.assertEqual(make_tree("session::var.foo").tree, ('(variable)', 'session', 'var.foo'))
		self.assertEqual(make_tree("request::var.s").tree, ('(variable)', 'request', 'var.s'))
		self.assertEqual(make_tree("rs::a.b.c.d.e").tree, ('(variable)', 'rs', 'a.b.c.d.e'))

	
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
