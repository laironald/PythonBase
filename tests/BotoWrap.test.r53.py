#!/usr/bin/python

import unittest
import os
import sys
sys.path.append("..")
import BotoWrap

class TestBotoWrap(unittest.TestCase):

    def removeTests(self, b):
        hosts = b.getHost("test_")
        if hosts:
            for h in hosts:
                b.r53.delete_hosted_zone(h)

    def setUp(self):
        self.aws = BotoWrap.BotoWrap()
        self.removeTests(self.aws)
        self.aws.r53.create_hosted_zone(domain_name="test_1.com")
        self.aws.r53.create_hosted_zone(domain_name="test_2.com")

    def tearDown(self):
        self.removeTests(self.aws)

    #======================================= Route 53

    def test_getHost(self):
        self.assertEquals(2, len(self.aws.getHost("test_")))
        self.assertEquals("Z", self.aws.getHost("test_1.com")[0])
        self.assertEquals(None, self.aws.getHost("foo.bar"))

if __name__ == '__main__':
    unittest.main()
