#!/usr/bin/env python

#  example test using Tester class

from ACR.utils.tester import Tester

def testExPositive():
  # the simpliest example of testing function
  # it should always return True, if the test was succedeed.
  # Otherwise, return False
  return 1 == 1

def testExNegative():
  return 2 < 1

def mySetUp():
  print "Setting env..."
    
def myCleanUp():
  print "Cleaning up env..."

def doTests():
  tester = Tester("simpleTestSuite")
  tester.addTest(testExPositive).addTest(testExNegative).setUp(mySetUp).cleanUp(myCleanUp)
  tester.run()