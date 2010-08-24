#!/usr/bin/env python
# -*- coding: utf-8 -*-

# AsynCode Framework - XML framework allowing developing internet
# applications without using programming languages. 
# Copyright (C) 2008-2010  Adrian Kalbarczyk, Marcin Radecki

# This program is free software: you can redistribute it and/or modify
# it under the terms of the version 3 of GNU General Public License as published by
# the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# TODO:
# 

from time import time

__all__ =  ["Tester",]

def __emptyFunc():
    pass

class Tester:
    """
    Simple class for doing unit tests.
    
    You can use this class by adding each of your test
    to set of all tests, which are being executed
    one by one.
    """
    
    def __init__(self, name):
        # list of tests (functions)
        self.testList = []
        # amount of each test should be executed
        self.countTestList = []
        # name of test-set
        self.name = name
        # cleanup and setup func
        self.cleanup = None
        self.setup = None
    
    def setUp(self, setupProc):
        """
        Sets up an testing environment.
        setupProc is function taking no arguments, where
        must be every task which should be done before test run.
        """
        
        self.setup = setupProc
        return self
    
    def cleanUp(self, cleanupProc):
        """
        Cleans up an testing environment. Here it must be
        every task which should be done after run all of tests.
        """
        
        self.cleanup = cleanupProc
        return self
    
    
    
    def addTest(self, test, count=1):
        """
        Adds a test to test-set. Optional parameter count
        means how many times test should be run.
        Single test must return True when its a positive.
        Any other case(False, and also raised exception)
        is treated as failed test.
        """
        
        if str(type(test)) != '<type \'function\'>':
            raise Exception("Given not a function.")
        self.testList.append(test)
        self.countTestList.append(count)
        
        return self
        
    def removeTest(self, test):
        """
        Removes a test from the test-set
        """
        
        if not test in self.testList:
            raise Exception("There is not such a given test.")
        i = self.testList.index(test)
        self.testList.pop(i)
        self.countTestList.pop(i)
        
        return self
    
    def __runSingleTest(self, test):
        # runs single test
        try:
            ret = test()
            if ret == True:
                # above condition is obligatory, because ret can be None
                return True
            else:
                return False
        except Exception:
            return False
    
    def __nrToStr(self, nr):
        if nr == 1:
            return '1st'
        elif nr == 2:
            return '2nd'
        else:
            return str(nr) + 'th'
    
    def run(self, count=1):
        """
        Runs all tests. Optional parameter count means
        how many times set of all tests should be executed.
        """
        if self.setup != None:
            self.setup()
        amountGlobal = 0
        amountGlobalFailed = 0
        start = time()
        for i in range(0,count):
            amountFailed = 0
            amountAll = 0
            startTestSet = time()
            print "Started test suite %s, %s time" % (self.name, self.__nrToStr(i+1))
            for j in range(0, len(self.testList)):
                # run single test countTestList times
                startSingleTest = time()
                ret = 'ok'
                amountAll += 1
                for k in range(0,self.countTestList[j]):
                    if self.__runSingleTest(self.testList[j]) == False:
                        ret = 'FAILED'
                        amountFailed += 1
                        break
                endSingleTest = time()
                print "%s: %s %.2f" % (str(self.testList[j]).split(" ")[1], ret, endSingleTest - startSingleTest)
            amountGlobal += amountAll
            amountGlobalFailed += amountFailed
            endTestSet = time()
            print "Result: %.2f correctness." % ((amountAll - amountFailed)/float(amountAll) * 100.0)
            print "Ended test suite in %.2f\n" % (endTestSet - startTestSet)
        if count > 1:
            # prints globals statistic
            print "Overall corectness: %.2f" % ((amountGlobal - amountGlobalFailed)/float(amountGlobal) * 100.0)
        if self.cleanup != None:
            self.cleanup()
               
def assertTrue(cond, msg):
    pass