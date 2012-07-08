#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2012 Clean ubuntu 11.10 <ptr@ubuntu>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

import time
import boto
import boto.ec2
import boto.route53
import re
import os
import sys

class BotoWrap:
    """Global variables:
        s3 = S3 connection
        bucket - S3 bucket

        r53 = Route53 
        host = hosted zone id
    """

    s3 = None
    r53 = None

    def __init__(self, bucket=None, host=None):
        """ 
        Args: 
            bucket: if bucket exists w/o permission, raises boto error.
                "new" means create new folder (smetrics_x) | x=time
                default: smetrics_default (for S3)
            host: the hosted zone id (for R53)
        """
        # S3
        self.s3 = boto.connect_s3()	
        if not bucket: 
            bucket = "smetrics_default"
        elif bucket == "new": 
            bucket = "smetrics_" + str(time.time())
        self.setBucket(bucket)

        # R53
        self.r53 = boto.connect_route53()
        self.setHost(host)

    def __del__(self):
        pass

    #======================================= Route 53

    def _retVarList(self, list):
        """ 
        Checks a list.  
        If single item, return the item.  If blank, return None.  
        Else. return the entire list.
        **Chosen not to test
        """
        if len(list) == 0:
            return None
        elif len(list) == 1:
            return list[0]
        else:
            return list

    #======================================= Route 53

    def _r53record(self, host, value, **kwargs):
        """ 
        Performs the commit necessary to modify Route 53
        """
        xchg = self.r53.get_all_rrsets(host)
        chg = xchg.add_change(**kwargs)
        for v in value.split(","):
            chg.add_value(v)
        try:
            xchg.commit()
        except:
            print "ERROR:", kwargs, value

    def getHostDomain(self, host=None):
        """ Get the domain name        
          Returns: domain name
        """
        if not host:
            host = self.host
        return self.r53.get_hosted_zone(host)["GetHostedZoneResponse"]["HostedZone"]["Name"]
             
    def getHost(self, host=None, **kwargs):
        """Get the Host Zone ID for the host specified

        Args:
            host: the name (or partial name) of a domain name
              if blank, defaults to the first Hosted Zone
        Returns:
            a list that represents the Host Ids
        """
        hosts = self.r53.get_all_hosted_zones(**kwargs)
        hosts = hosts.ListHostedZonesResponse.HostedZones
        list = []

        if not host:
            list.append(hosts[0].Id)
        else:
            for h in hosts:
                #for convenience purposes, note: this may create duplication issues
                if h.Name.find(host) == 0:
                    list.append(h.Id)

        list = [h.replace("/hostedzone/", "") for h in list]
        return list

    def setHost(self, host=None):
        """ 
        Set default hosted zone id. If domain is provided find and set appropriately

        Args: 
          host: the name (or hosted zone id)
        Returns:
          the hosted zone id
        """
        try:
            self.r53.get_hosted_zone(host)
            self.host = host
        except:
            self.host = self.getHost(host)[0]
        return self.host

    def getRecordSet(self, host=None, **kwargs):
        """ 
        fetch record sets that match the criteria specified

        Args:
          **name, type, ttl, value -> dict
          kwargs follows the values above
        Returns:
          List of record arguments that fit the criteria per above
          if no criterias, return everything
        """
        if not host:
            host = self.host
        domain = self.getHostDomain(host)
        changes = self.r53.get_all_rrsets(host)
        list = []

        if "name" in kwargs:
            if not kwargs["name"]:
                kwargs["name"] = domain
            elif kwargs["name"].find(domain) == -1:
                kwargs["name"] = kwargs["name"] + "." + domain 

        for c in changes:
            ac = {"name": c.name, "type": c.type, 
                  "ttl": c.ttl, "value": c.to_print()}
            if set(kwargs.items()) <= set(ac.items()):
                list.append(ac)
            elif not kwargs:
                list.append(ac)
        return list

    def setRecordSet(self, name=None, value=None, host=None, template=None, **kwargs):
        """ 
        create new record sets (or delete), depending on action

        Args:
          **action, name, type, ttl -> dict (kwargs)
          name: the subdomain
          value: the entry of the recordset

          template: 
            gmail: creates mail.domain.com > for Google Apps access

          **note either template OR name+value are required
        """
        if not host:
            host = self.host
        domain = self.getHostDomain(host)
        changes = self.r53.get_all_rrsets(host)

        if value:
            if not name:
                name = domain
            elif name.find(domain) == -1:
                #if it appears just to be a subdomain
                name = name + "." + domain 

            if "action" not in kwargs:
                kwargs["action"] = "CREATE"
            if "ttl" not in kwargs:
                kwargs["ttl"] = "300"
            if "type" not in kwargs:
                # if IP address
                if re.findall("([0-9]+[.]){3}[0-9]+", value):
                    kwargs["type"] = "A"
                # if any dots assume CNAME
                elif len(value.split(".")) > 1:
                    kwargs["type"] = "CNAME"
                else:
                    kwargs["type"] = "TXT"

            self._r53record(host, name=name, value=value, **kwargs)
        elif template == "gmail":
            self._r53record(host, action="CREATE", name="mail."+domain, 
                type="CNAME", value="ghs.googlehosted.com")
            self._r53record(host, action="CREATE", name=domain, type="MX", ttl="300",
                value="1 ASPMX.L.GOOGLE.COM.,5 ALT1.ASPMX.L.GOOGLE.COM.,5 ALT1.ASPMX.L.GOOGLE.COM.,10 ASPMX2.GOOGLEMAIL.COM.,10 ASPMX3.GOOGLEMAIL.COM.")

    def updateRecordSet(self, criteria, to={}, host=None):
        """ 
        update a record set
       
        Args:
          **name, type, ttl, value -> dict
          criteria: dictionary with keys above to modify
          to: dictionary with keys above to change
          host: modify the hosted zone id
        """
        if not host:
            host = self.host


        changes = self.r53.get_all_rrsets(host)
        #find recsets
        for c in changes:
            ac = {"name": c.name, "type": c.type, 
                  "ttl": c.ttl, "value": c.to_print()}
            if set(criteria.items()) <= set(ac.items()):
                self._r53record(host, action="DELETE", **ac)
                for k in to:
                    ac[k] = to[k]
                self._r53record(host, action="CREATE", **ac)

    #======================================= S3

    def setBucket(self, bucket):
        """set Bucket
        Args:
            bucket: name of the bucket to change
        """
        self.bucket = self.s3.create_bucket(bucket)

    def getBucket(self, bucket=None, set=True):
        """return Bucket
        Args:
            bucket: name of the bucket to fetch
        Returns: bucket object (default is default bucket)
        """
        if bucket:
            return self.s3.create_bucket(bucket)
        else:
            return self.bucket

    def getS3key(self, key, bucket=None):
        """Get corresponding S3 key

        Args:
            key: in S3 vocabulary, the key accesses the S3 data
            bucket: specified S3 bucket name (else: default)

        Returns: key for further manipulations
        """
        k = self.getBucket(bucket).get_key(key)
        return k

    def downloadS3(self, key, file=None, bucket=None, path=None,
                   debug=False, override=False):
        """Download a file from AWS to the local server

        Args:
            key: the location of the file on S3.  
            file: the file to be transferred
                default: to be the same as key.
            bucket: specified bucket name.
                default: smetrics_default
            path: a location outside of the root directory (for key)
            permission: sets the ACL
                default: authenticated-read
                other options: public-read, public-read-write, private
            override: allow files to be overwritten?  
                otherwise check size/time before overwritting happens

        Returns: key associated with upload
        Raises: No current Error handling.
        """
        def overrideIt(k):
            # file worth overriding?
            # override and file should be static global variables
            if override: return True 
            if not k: return False
            if not k.exists(): return False
            if not os.path.isfile(file): return True
            #sequence makes a difference here..
            #time zone makes this challenging..
            kTime = time.mktime(time.strptime(
                         k.last_modified, "%a, %d %b %Y %H:%M:%S %Z"))
            kSize = k.size
            if os.path.getsize(file) != kSize and \
               os.path.getmtime(file) < kTime:
                return True
            return False

        # TODO(ron): if key contains invalid characters (unicode). 
        #            that creates problems with rendering buckets.  deal!
        if not file: file = key
        bucket = self.getBucket(bucket)
        if path:
            key = "{path}/{key}".format(path=path, key=key)
           
        if debug: print "S3:", file, key,
        k = self.bucket.get_key(key)

        if overrideIt(k):
            #get cwd of file
            file_cwd = "/".join(file.split("/")[0:-1])
            #blank file_cwd means on root path.  this is OK
            if file_cwd and not os.path.exists(file_cwd):
                os.makedirs(file_cwd)
            k = bucket.new_key(key)
            k.get_contents_to_filename(file)
            if debug: print "[downloaded]",
        if debug: print ""

    def downloadS3_path(self, dir="", bucket=None, path=None, **kwargs):
        """Downloads a path (and its contents) to S3

        Args:
            dir: the directory to be inspected
                default: the current directory (also known as ".")
            recursive: allows recursive searching of directory
        Returns: No current return.
        Raises: No current Error handling.
        """
    
        cBucket = self.getBucket(bucket)
        for k in cBucket.get_all_keys(prefix=dir):
            key = k.name
            #specified path allows a full path to not be generated
            # ie. S3 boto/ron > path=boto > ron
            if path:
                key = re.sub("^"+path, "", key)
                key = re.sub("^/", "", key)           
            self.downloadS3(key=key, bucket=bucket, path=path, **kwargs)

    def uploadS3(self, file, key=None, bucket=None, path=None, encrypt=False,
                 permission="authenticated-read", debug=False, override=False):
        """Upload a file from the local server to AWS

        Args:
            file: the file to be transferred
            key: the location of the file on S3.  
                default: to be the same as file.
            bucket: specified bucket name.
                default: smetrics_default
            path: a location outside of the root directory
            encrypt: do we encrypt the data? (AES-256)
            permission: sets the ACL
                default: authenticated-read
                other options: public-read, public-read-write, private
            override: allow files to be overwritten?  
                otherwise check size/time before overwritting happens

        Returns: key associated with upload
        Raises: No current Error handling.
        """
        def overrideIt(k):
            # file worth overriding?
            # override and file should be static global variables
            if override: return True 
            if not k: return True
            if not k.exists(): return True
            # if size or time parameters change or key doesn't exist
            kTime = time.mktime(time.strptime(
                         k.last_modified[:-4], "%a, %d %b %Y %H:%M:%S"))
            kSize = k.size
            if os.path.getsize(file) != kSize or \
               os.path.getmtime(file) > kTime:
                return True
            return False

        # TODO(ron): if key contains invalid characters (unicode). 
        #            that creates problems with rendering buckets.  deal!
        if not key: key = file
        bucket = self.getBucket(bucket)
        if path: 
            key = "{path}/{file}".format(path=path, file=key)

        if debug: print "S3:", bucket, file, key,
        if os.path.isfile(file):
            # must get file to get its attributes
            k = bucket.get_key(key)     
            # if size or time parameters change or key doesn't exist
            if overrideIt(k):
                k = bucket.new_key(key)
                k.set_contents_from_filename(file, encrypt_key=encrypt)
                k.set_acl(permission)
                if debug: print "[uploaded]",
        if debug: print ""

    def uploadS3_path(self, dir=".", recursive=True, **kwargs):
        """Uploads a path (and its contents) to S3

        Args:
            dir: the directory to be inspected
                default: the current directory (also known as ".")
            recursive: allows recursive searching of directory
        Returns: No current return.
        Raises: No current Error handling.
        """
        for x in os.listdir(dir):
            if dir == ".":
                obj = x
            else:
                obj = "{dir}/{file}".format(dir=dir, file=x)
            if os.path.isfile(obj):
                self.uploadS3(file=obj, **kwargs)
            elif recursive:
                self.uploadS3_path(dir=obj, recursive=recursive, **kwargs)

    #===============================================================

    def checkSysStatus(self, instance):
        time.sleep(120)
        out = instance.get_console_output()
        m = re.search('([0-9a-f][0-9a-f]:){15}[0-9a-f][0-9a-f]', 
                      str(out.output))
        os.popen("ssh-keyscan %s 2>/dev/null > host.key" % 
                 instance.public_dns_name)
        os.popen("ssh-keygen -q -R %s" % instance.public_dns_name)
        os.popen("ssh-keygen -q -H -f host.key")
        os.popen("cat host.key >> ~/.ssh/known_hosts")
        #ignore for now, checking validity of host key
        #os.popen("ssh-keygen -lf host.key > host.fingerprint")
        #os.popen("read len ACTUAL_FINGERPRINTS host rsa < host.fingerprint")
        #os.popen('echo "Actual fingerprints are $ACTUAL_FINGERPRINTS"')
        #print "Actual fingerprints are $ACTUAL_FINGERPRINTS"

    def checkKeyPair(self, keypair_name, public_key_file):
        fp = open(public_key_file)
        material = fp.read()
        fp.close()
        for region in boto.ec2.regions():
            ec2 = region.connect()
            try:
                key = ec2.get_all_key_pairs(keynames=[keypair_name])[0]
                print 'Keypair(%s) already exists in %s' % \
                       (keypair_name, region.name)
            except ec2.ResponseError, e:
                if e.code == 'InvalidKeyPair.NotFound':
                    print 'Importing keypair(%s) to %s' % \
                          (keypair_name, region.name)
            ec2.import_key_pair(keypair_name, material)

    def startEC2Instance(self, 
                         ami="ami-2727f84e", key_name="automation-key3", 
                         instance_type="t1.micro", group_name = "open5",
                         key_extension=".pem", key_dir="~/.ssh", 
                         ssh_port=22, solr_port=8983, http_port=80,
                         tag="instance test", cidr = "0.0.0.0/0", 
                         user_data="None", login_usr="ubuntu"):
        ec2 = boto.connect_ec2()
        try:
            key = ec2.get_all_key_pairs(keynames=[key_name])[0]
        except ec2.ResponseError, e:
            if e.code == 'InvalidKeyPair.NotFound':
                print 'Creating keypair: %s' % key_name
                key = ec2.create_key_pair(key_name)
                key.save(key_dir)
        try:
            group = ec2.get_all_security_groups( groupnames=[group_name])[0]
        except ec2.ResponseError, e:
            if e.code == "InvalidGroup.NotFound" :
                print "Creating Security Group: %s" % group_name
                group = ec2.create_security_group(group_name, "A group that allows ssh access")
                group.authorize("tcp", ssh_port, ssh_port, cidr)
                group.authorize("tcp", solr_port, solr_port, cidr)
                group.authorize("tcp", http_port, http_port, cidr)
            else:
                raise

        reservation = ec2.run_instances(ami, key_name=key_name, 
                                        security_groups=[group_name], 
                                        instance_type=instance_type, 
                                        user_data=user_data)
        instance = reservation.instances[0]
        print 'waiting for instance to start'
        while instance.state != 'running':
            print "Instance state =" + str(instance.state)
            time.sleep(5)
            instance.update()
        print "done"

        print "DNS = " + str(instance.public_dns_name)
        #instance.use_ip("23.21.137.252")
        instance.add_tag( tag )	
        time.sleep(10)
        self.checkSysStatus(instance)
        return instance.public_dns_name

    #from cookbook
    def printRunningInstances(self, running_instances):
        print 'The following running instances were found'
        for account_name in running_instances:
            print '\tAccount: %s' % account_name
            d = running_instances[account_name]
            for region_name in d:
                print '\t\tRegion: %s' % region_name
                for instance in d[region_name]:
                    print '\t\t\tAn %s instance: %s' % \
                          (instance.instance_type, instance.id)
                    print '\t\t\t\tTags=%s' % instance.tags	

    #account_name[array]->Region[array]->instance/tag		
    def findAllRunningInstances(self, accounts=None, quiet=False):
        """
        Will find all running instances across all EC2 regions for all of the
        accounts supplied.

        :type accounts: dict
        :param accounts: A dictionary contain account information.  The key is
                         a string identifying the account (e.g. "dev") and the
                         value is a tuple or list containing the access key
                         and secret key, in that order.
                         If this value is None, the credentials in the boto
                         config will be used.
        """
        if not accounts:
            creds = (boto.config.get('Credentials', 'aws_access_key_id'),
                     boto.config.get('Credentials', 'aws_secret_access_key'))
            accounts = {'main' : creds}
        running_instances = {}
        for account_name in accounts:
            running_instances[account_name] = {}
            ak, sk = accounts[account_name]
            for region in boto.ec2.regions():
                conn = region.connect(aws_access_key_id=ak, 
                                      aws_secret_access_key=sk)
                filters={'instance-state-name' : 'running'}
                instances = []
                reservations = conn.get_all_instances(filters=filters)
                for r in reservations:
                    instances += r.instances
                if instances:
                    running_instances[account_name][region.name] = instances
        if not quiet:
            self.printRunningInstances(running_instances)
        return running_instances

    def terminateInstances(self, instanceId):
        ec2 = boto.connect_ec2()
        for account_name in instanceId:
            print '\tAccount: %s' % account_name
            d = instanceId[account_name]
            for region_name in d:
                print '\t\tRegion: %s' % region_name
                for instance in d[region_name]:
                    print '\t\t\tAn %s instance: %s' % \
                          (instance.instance_type, instance.id)
                    print '\t\t\t\tTags=%s' % instance.tags	
                    print '\nTerminating instance "%s"' % instance.id
                    ret = ec2.terminate_instances(str(instance.id))
                    print "Terminated instance %s" % ret
		
