#!/usr/bin/python

import BotoWrap
import unittest
import os
import sys

class TestBotoWrap(unittest.TestCase):

    def setUp(self):
        self.aws = BotoWrap.BotoWrap(bucket="smetrics_test")
        #s3
        os.system("touch file.test")
        os.system("mkdir tempDIRtemp")
        os.system("touch tempDIRtemp/file1.test")
        os.system("touch tempDIRtemp/file2.test")
        os.system("mkdir tempDIRtemp/DIR")
        os.system("touch tempDIRtemp/DIR/file3.test")
        self.key1 = self.aws.bucket.new_key("key1.test")
        self.key1.set_contents_from_filename("file.test")
        self.key2 = self.aws.bucket.new_key("key/key2.test")
        self.key2.set_contents_from_filename("file.test")

    def tearDown(self):
        #s3
        os.system("rm file.test")
        os.system("rm tempDIRtemp/file1.test")
        os.system("rm tempDIRtemp/file2.test")
        os.system("rm tempDIRtemp/DIR/file3.test")
        os.system("rmdir tempDIRtemp/DIR")
        os.system("rmdir tempDIRtemp")
        self.key1.delete()
        self.key2.delete()

    #======================================= S3

    def s3KeyCheck(self, key, bucket=None, remove=True, acl=None):
        #easy test to see if a certain file exists
        bucket = self.aws.getBucket(bucket)
        k = bucket.get_key(key)
        if not k:
            return False
        if not k.exists():
            return False
        # TODO (ron): how do we return this in a meaningufl way?
        #if acl:
        #    print k.get_acl()
        if remove:
            k.delete()
        return True

    def test_getS3key(self):
        self.aws.uploadS3("file.test")
        key = self.aws.getS3key("file.test")
        # make sure key is being returned
        self.assertEqual(str(type(key)), "<class 'boto.s3.key.Key'>")
        # remove the key
        key.delete()

    def test_downloadS3(self):
        #default file
        self.aws.downloadS3("key1.test")
        #default file under a folder key
        self.aws.downloadS3("key/key2.test")
        #default file under a path
        self.aws.downloadS3("key2.test", path="key")
        #change default file name
        self.aws.downloadS3("key1.test", file="key1.testy")
        self.aws.downloadS3("key/key2.test", file="key2.testy")
        self.assertTrue(os.path.isfile("key/key2.test"))
        self.assertTrue(os.path.isfile("key1.test"))
        self.assertTrue(os.path.isfile("key2.test"))
        self.assertTrue(os.path.isfile("key1.testy"))
        self.assertTrue(os.path.isfile("key2.testy"))
        os.system("rm -rf key")
        os.system("rm key1.test")
        os.system("rm key2.test")
        os.system("rm key1.testy")
        os.system("rm key2.testy")
        # TODO(ron): override permissions?  what's intuitive?

    def test_downloadS3_path(self):
        # TODO(ron): 
        pass

    def test_uploadS3(self):
        # default settings
        self.aws.uploadS3("file.test")
        self.assertTrue(self.s3KeyCheck("file.test"))
        # change the default key
        self.aws.uploadS3("file.test", key="file.test2")
        self.assertTrue(self.s3KeyCheck("file.test2"))
        # change the default bucket
        self.aws.uploadS3("file.test", bucket="smetrics_test2")
        self.assertTrue(self.s3KeyCheck("file.test", 
                                        bucket="smetrics_test2"))
        self.aws.s3.delete_bucket("smetrics_test2")
        # change the default path
        self.aws.uploadS3("file.test", path="smetrics_test")
        self.assertTrue(self.s3KeyCheck("smetrics_test/file.test"))
        # few key + path combos
        self.aws.uploadS3("file.test", path="smetrics_test", key="f.test")
        self.assertTrue(self.s3KeyCheck("smetrics_test/f.test"))
        self.aws.uploadS3("file.test", path="smetrics_test/test", 
                                       key="file.test")
        self.assertTrue(self.s3KeyCheck("smetrics_test/test/file.test"))
        self.aws.uploadS3("file.test", key="smetrics_test/file.test/test")
        self.assertTrue(self.s3KeyCheck("smetrics_test/file.test/test"))
        # change of permission
        # TODO (ron): test for change of permission
        #self.aws.uploadS3("file.test", permission="private")
        #self.assertTrue(self.s3KeyCheck("file.test", acl="private"))

    def test_uploadS3_path(self):
        # test generic file load (3 files)
        self.aws.uploadS3_path("tempDIRtemp")
        k = self.aws.bucket.get_all_keys()
        self.assertEqual(len(k), 5) #test, has 5
        for x in k: x.delete()      #delete

        # test if from default path
        os.chdir("tempDIRtemp")
        self.aws.uploadS3_path()
        k = self.aws.bucket.get_all_keys()
        self.assertEqual(len(k), 3)
        for x in k: x.delete()
        os.chdir("..")

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

    if len(sys.argv) > 1:
        # if we specify a specific testing group ie. ./BotoWrap.test.py s3
        tests = unittest.TestSuite()
        if sys.argv[1].lower() == "s3":
            tests.addTest(TestBotoWrap('test_getS3key'))
            tests.addTest(TestBotoWrap('test_downloadS3'))
            tests.addTest(TestBotoWrap('test_downloadS3_path'))
            tests.addTest(TestBotoWrap('test_uploadS3'))
            tests.addTest(TestBotoWrap('test_uploadS3_path'))
        elif sys.argv[1].lower() == "r53":
            tests.addTest(TestBotoWrap('test_getHost'))
        unittest.TextTestRunner().run(tests)
    else:
        unittest.main()


