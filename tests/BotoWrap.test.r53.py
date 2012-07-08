#!/usr/bin/python

import unittest
import os
import sys
sys.path.append("..")
import BotoWrap

class TestBotoWrap(unittest.TestCase):

    def removeTests(self):
        hosts = self.aws.getHost("test_")
        if hosts:
            for h in hosts:
                self.aws.r53.delete_hosted_zone(h)

    def setUp(self):
        self.aws = BotoWrap.BotoWrap()
        self.removeTests()
        self.aws.r53.create_hosted_zone(domain_name="test_1.com")
        self.host = self.aws.getHost("test_1")[0]

    def tearDown(self):
        self.removeTests()

    #======================================= Route 53

    def test_getHost(self):
        self.aws.r53.create_hosted_zone(domain_name="test_2.com")
        self.assertEquals(2, len(self.aws.getHost("test_")))
        self.assertEquals("Z", self.aws.getHost("test_1.com")[0][0])
        self.assertEquals([], self.aws.getHost("foo.bar"))
        self.removeTests()

    def test_setHost(self):
        #make sure returns a host
        self.assertEquals("Z", self.aws.setHost(None)[0])

    def test_setRecordSet(self):
        self.aws.setHost(self.host)
        self.aws.setRecordSet(template="gmail")
        self.aws.setRecordSet(value="2.1.1.1")
        self.aws.setRecordSet(name="ww1", value='"ron"')
        self.aws.setRecordSet(name="ww2", value="ron.con.com")
        self.aws.setRecordSet(name="ww3", value="1.1.1.1")
        self.assertEquals("TXT", self.aws.getRecordSet(name="ww1")[0]["type"])
        self.assertEquals("CNAME", self.aws.getRecordSet(name="ww2")[0]["type"])
        self.assertEquals("CNAME", self.aws.getRecordSet(name="mail")[0]["type"])     
        self.assertEquals("A", self.aws.getRecordSet(name="ww3")[0]["type"])
        self.assertEquals("A", self.aws.getRecordSet(value="2.1.1.1")[0]["type"])
        self.aws.setRecordSet(value="2.1.1.1", action="DELETE")
        self.aws.setRecordSet(action="DELETE", **self.aws.getRecordSet(name="ww1")[0])
        self.aws.setRecordSet(action="DELETE", **self.aws.getRecordSet(name="ww2")[0])
        self.aws.setRecordSet(action="DELETE", **self.aws.getRecordSet(name="ww3")[0])
        self.aws.setRecordSet(action="DELETE", **self.aws.getRecordSet(name="mail")[0])
        self.aws.setRecordSet(action="DELETE", **self.aws.getRecordSet(type="MX")[0])

    def test_getHostDomain(self):
        self.assertEquals("test_1.com.", self.aws.getHostDomain(self.host))

    def test_getRecordSet(self):
        self.aws.setHost(self.host)
        self.assertEquals(2, len(self.aws.getRecordSet()))
        self.assertEquals(2, len(self.aws.getRecordSet(name="")))
        self.assertEquals(1, len(self.aws.getRecordSet(type="NS")))

    def test_updateRecordSet(self):       
        self.aws.setRecordSet(name="ww1", value='"ron"')
        self.aws.setRecordSet(name="ww2", value='"ron"')
        self.aws.updateRecordSet(
            criteria={"type":"TXT"}, to={"value":'"foobar"'})

if __name__ == '__main__':
    unittest.main()
