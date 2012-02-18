import unittest
from tulip import Tulip
import re


class TulipTestCases(unittest.TestCase):

    def setUp(self):
        self.tulip = Tulip()
        self.reg = re.compile(r'addRow\(([\w \',.]+)\)')
        f = open('tulipv3vee1.out')
        self.fileString = f.read()

    def testRegex(self):
        f = open('tst.txt')
        inputString = f.readline()
        matchList = f.readline().strip().split(',')
        result = self.reg.match(inputString)
        assert matchList == result.group(1).split(',')
    def testGetServers(self):
        out = self.tulip.getServers(self.fileString)
        #print out
    def testGetCoords(self):
        out = self.tulip.getLocation(self.fileString)
        #print out
    def testGetRandomIP(self):
        self.tulip.getHostInfo('v3vee.org')
        #print self.tulip.getAddress('8.8.8.8')
    def testGetFailedIP(self):
        assert self.tulip.getHostInfo('9.34.6.5') is None
        #assert 'Unable to get 3 minimun rtt values'  in x
            
    


if __name__=="__main__":
    unittest.main()

