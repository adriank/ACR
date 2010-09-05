#!/usr/bin/env python

from ACF.utils.tester import Tester
from ACF.utils.interpreter import *
from random import randint, choice
import sys

# change a global settings - depth of recursion
sys.setrecursionlimit(20000)

# helper functions for creating correctness tests
def generate():
	file = open('test', 'w')
	print 'Testing parser. Enter a program or \'q\' for exit.'
	while 1:
		s = raw_input("program: ")
		if s == 'q':
			break
		ans = make_tree(s)
		print "Answer: %s. Correct [y|n] ?" % str(ans),
		yesno = raw_input()
		if yesno == 'y':
			file.write('assert(make_tree("%s") == %s)\n' % (s,ans))
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
def generateVar():
	s = '{$'
	if (randint(0,1) == 0): # with storage
		s += choice(['ss', 'rs', 'session', 'request']) + '::'
	for i in range(0, randint(1,5)):
		s += choice('abcde') + '.'
	return s[0:-1] + '}' # without last character (dot)

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

# corectness tests		
# associativity, addition, subtraction, multiplication, division, name literals
def test_correct1():
	assert(make_tree("2+3") == ('+',2,3))
	assert(make_tree("2+(3+4)") == ('+', 2, ('+', 3, 4)))
	assert(make_tree("2+3+4") == make_tree("(2+3)+4"))
	assert(make_tree("2-3+4+5-7") == ('-', ('+', ('+', ('-', 2, 3), 4), 5), 7))
	assert(make_tree("33*2/5-2") == ('-', ('/', ('*', 33, 2), 5), 2))
	assert(make_tree("33-4*5+2/6") == ('+', ('-', 33, ('*', 4, 5)), ('/', 2, 6)))
	assert(make_tree("(33-4)*5+2/6") == ('+', ('*', ('-', 33, 4), 5), ('/', 2, 6)))
	assert(make_tree("2//3//4//5") == ('//', ('//', ('//', 2, 3), 4), 5))
	assert(make_tree("abc + def") == ('+', ('name', 'abc'), ('name', 'def')))
	assert(make_tree("(f+b)+f+(c+(d+e))") == ('+', ('+', ('+', ('name', 'f'), ('name', 'b')), ('name', 'f')), ('+', ('name', 'c'), ('+', ('name', 'd'), ('name', 'e')))))
	assert(make_tree("2/3/(4/5)*6") == ('*', ('/', ('/', 2, 3), ('/', 4, 5)), 6))
	assert(make_tree("((2+4))+6") == ('+', ('+', 2, 4), 6))
	return True

# not, or, and, not in ,is not
def test_correct2():
	assert(make_tree("1 or 2 or 3") == ('or', 1, ('or', 2, 3)))
	assert(make_tree("1 and (2 and 3)") == ('and', 1, ('and', 2, 3)))
	assert(make_tree("(1 and 2) or 3") == ('or', ('and', 1, 2), 3))
	assert(make_tree("not 1 and 2") == ('and', ('not', 1), 2))
	assert(make_tree("not (1 and 2)") == ('not', ('and', 1, 2)))
	assert(make_tree("(not 1) and 2") == ('and', ('not', 1), 2))
	assert(make_tree("1 + 2 or 3 / (not 4)") == ('or', ('+', 1, 2), ('/', 3, ('not', 4))))
	assert(make_tree("4     and 5       - 1") == ('and', 4, ('-', 5, 1)))
	assert(make_tree("foo not in bar") == ('not in', ('name', 'foo'), ('name', 'bar')))
	assert(make_tree("23 is not 56 or 25 is 57") == ('or', ('is not', 23, 56), ('is', 25, 57)))
	assert(make_tree("2 is 3 is not (not 5)") == ('is not', ('is', 2, 3), ('not', 5)))
	assert(make_tree("not not not 7") == ('not', ('not', ('not', 7))))
	assert(make_tree("(foo is bar) and (foo is not bar) or 6") == ('or', ('and', ('is', ('name', 'foo'), ('name', 'bar')), ('is not', ('name', 'foo'), ('name', 'bar'))), 6))
	assert(make_tree("2+3/4-6*7 or 10 is not 11 and 14") == ('or', ('-', ('+', 2, ('/', 3, 4)), ('*', 6, 7)), ('and', ('is not', 10, 11), 14)))
	return True

# <, >, <=, >=, prefix: +, - ~
def test_correct3():
	assert(make_tree("~2 + +3") == ('+', ('~', 2), ('+', 3)))
	assert(make_tree("++3") == ('+', ('+', 3)))
	assert(make_tree("-+-3") == ('-', ('+', ('-', 3))))
	assert(make_tree("34//22 + foo < 67-(     bar is not 2)") == ('<', ('+', ('//', 34, 22), ('name', 'foo')), ('-', 67, ('is not', ('name', 'bar'), 2))))
	assert(make_tree("2 < 3 < 4 < 5") == ('<', ('<', ('<', 2, 3), 4), 5))
	assert(make_tree("2 >= 1 or +1") == ('or', ('>=', 2, 1), ('+', 1)))
	assert(make_tree("1 <= (2 <= 3)") == ('<=', 1, ('<=', 2, 3)))
	assert(make_tree("+1 <= ~2 > -3") == ('>', ('<=', ('+', 1), ('~', 2)), ('-', 3)))
	return True

# [], . , tuples, lists
def test_correct4():
	assert(make_tree("(2, foo, 4)") == ('(', [2, ('name', 'foo'), 4]))
	assert(make_tree("[bar, 2, foo]") == ('[', [('name', 'bar'), 2, ('name', 'foo')]))
	assert(make_tree("object.variable + 2 - list[0]") == ('-', ('+', ('.', ('name', 'object'), ('name', 'variable')), 2), ('[', ('name', 'list'), 0)))
	assert(make_tree("list[2][2][3]") == ('[', ('[', ('[', ('name', 'list'), 2), 2), 3))
	assert(make_tree("list[6].object[1] <= 1111111") == ('<=', ('[', ('.', ('[', ('name', 'list'), 6), ('name', 'object')), 1), 1111111))	
	return True

# function calls, constnants
def test_correct5():
	assert(make_tree("f(2)") == ('(', [('name', 'f'), 2]))
	assert(make_tree("(f,)") == ('(', [('name', 'f')]))
	assert(make_tree("f()") == ('(', ('name', 'f')))
	assert(make_tree("2()") == ('(', 2))
	assert(make_tree("f(2<3)") == ('(', [('name', 'f'), ('<', 2, 3)]))
	assert(make_tree("f(g())") == ('(', [('name', 'f'), ('(', ('name', 'g'))]))
	assert(make_tree("f(g(h(2)))") == ('(', [('name', 'f'), ('(', [('name', 'g'), ('(', [('name', 'h'), 2])])]))
	assert(make_tree("f() + g()*h()") == ('+', ('(', ('name', 'f')), ('*', ('(', ('name', 'g')), ('(', ('name', 'h')))))
	assert(make_tree("None") == None)
	assert(make_tree("True or False and None") == ('or', True, ('and', False, None)))
	assert(make_tree("~true") == ('~', ('name', 'true')))
	assert(make_tree("~True is not False") == ('is not', ('~', True), False))
	return True

# variables
def test_correct6():
	assert(make_tree("{$var}") == ('(variable)', 'rs', 'var'))
	assert(make_tree("{$var.foo.bar}") == ('(variable)', 'rs', 'var.foo.bar'))
	assert(make_tree("{$ss::var}") == ('(variable)', 'ss', 'var'))
	assert(make_tree("{$session::var.foo}") == ('(variable)', 'session', 'var.foo'))
	assert(make_tree("{$request::var}") == ('(variable)', 'request', 'var'))
	assert(make_tree("{$rs::x.y.z.d.e.f}") == ('(variable)', 'rs', 'x.y.z.d.e.f'))
	return True

# tests invalid expressions
def test_invalid():
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

# efficiency tests, reads data from file, which consists of two lines:
# first is data in, and second data out (expected out)
def test_efficiency(id):
	def new_test():
		file = open ('./ACF/test/test' + str(id), 'r')
		s1 = file.readline().rstrip()
		s2 = file.readline().rstrip()
		assert(str(make_tree(s1)) == s2)
		file.close()
		return True
	new_test.__name__ = 'test_efficiency' + str(id)
	return new_test

def doTests():
	tester = Tester("utils.interpreter")
	test_efficiency1 = test_efficiency(1)
	test_efficiency2 = test_efficiency(2)
	tester.addTest(test_correct1).addTest(test_correct2).addTest(test_correct3).addTest(test_correct4).addTest(test_correct5).addTest(test_correct6).addTest(test_invalid).addTest(test_efficiency1).addTest(test_efficiency2)
	tester.run()