#!/usr/bin/python

import unittest
import os
import sys
sys.path.append("..")
import BotoWrap

class TestBotoWrap(unittest.TestCase):

    def setUp(self):
        self.aws = BotoWrap.BotoWrap()

    def tearDown(self):
        pass

    #======================================= Route 53

    def test_getHost(self):
        #r53
        self.hosts = [self.aws.r53.create_hosted_zone(domain_name="test.com"),
                      self.aws.r53.create_hosted_zone(domain_name="test2.com")]

        print self.aws.getHost("test")
        print self.aws.getHost("test.com")
        print self.aws.host
        print self.aws.setHost("test")
        print self.aws.host
        #r53
        self.aws.r53.delete_hosted_zone(self.hosts[0].CreateHostedZoneResponse.HostedZone.Id.replace("/hostedzone/", ""))
        self.aws.r53.delete_hosted_zone(self.hosts[1].CreateHostedZoneResponse.HostedZone.Id.replace("/hostedzone/", ""))
        pass

if __name__ == '__main__':

    b = BotoWrap.BotoWrap()
    print b.getHost("test.com")
    print b.getHost("smetrics.org")
    print b.setHost("smetrics.org")
    print b.host

    fjkdsajflajladsjfldjs

    unittest.main()


