import boto.route53.record
import boto.route53
g = boto.route53.connection.Route53Connection()
host = g.get_hosted_zone(hosted_zone_id="Z6Q71ND65H5MS")
host.items()
# OUT: [(u'GetHostedZoneResponse', {u'HostedZone': {u'CallerReference': u'7A107689-F884-E1D4-B1E1-E91AB2F426FB', u'Config': {}, u'Id': u'/hostedzone/Z6Q71ND65H5MS', u'Name': u'laironald.com.'}, u'DelegationSet': {u'NameServers': [u'ns-1545.awsdns-01.co.uk', u'ns-1358.awsdns-41.org', u'ns-397.awsdns-49.com', u'ns-694.awsdns-22.net']}})]
boto.route53.record.ResourceRecordSets
# OUT: <class 'boto.route53.record.ResourceRecordSets'>
boto.route53.record.ResourceRecordSets()
# OUT: <ResourceRecordSets: None>
boto.route53.record.ResourceRecordSets(hosted_zone_id="Z6Q71ND65H5MS")
# OUT: <ResourceRecordSets: Z6Q71ND65H5MS>
boto.route53.record.ResourceRecordSets(hosted_zone_id="Z6Q71ND65H5MS")[0]
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: IndexError: list index out of range
boto.route53.record.ResourceRecordSets(hosted_zone_id="Z6Q71ND65H5MS")
# OUT: <ResourceRecordSets: Z6Q71ND65H5MS>
conn = boto.connect_route53()
boto.route53.record.ResourceRecordSets(conn, hosted_zone_id="Z6Q71ND65H5MS")
# OUT: <ResourceRecordSets: Z6Q71ND65H5MS>
changes = boto.route53.record.ResourceRecordSets(conn, hosted_zone_id="Z6Q71ND65H5MS")
changes.next_record_name()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: TypeError: 'NoneType' object is not callable
changes.next_record_name
changes
# OUT: <ResourceRecordSets: Z6Q71ND65H5MS>
changes.index
# OUT: <built-in method index of ResourceRecordSets object at 0x10a555208>
changes.index()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: TypeError: index() takes at least 1 argument (0 given)
changes.index(0)
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: ValueError: 0 is not in list
changes.index(1)
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: ValueError: 1 is not in list
changes.markers
# OUT: [('ResourceRecordSet', <class 'boto.route53.record.Record'>)]
changes.markers()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: TypeError: 'list' object is not callable
changes.markers[0]
# OUT: ('ResourceRecordSet', <class 'boto.route53.record.Record'>)
boto.config.get("dns", "name")
print boto.config.get("dns", "name")
# OUT: None
host.get_name("test.laironald.com")
# OUT: 'test.laironald.com'
host.has_key("test.laironald.com")
# OUT: False
changes.add_change(action='CREATE', name='laironald.com', type='A')
# OUT: <boto.route53.record.Record object at 0x10a55b850>
conn.get_all_rrsets(host_zone_id="Z6Q71ND65H5MS")
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: TypeError: get_all_rrsets() got an unexpected keyword argument 'host_zone_id'
conn.get_all_rrsets(hosted_zone_id="Z6Q71ND65H5MS")
# OUT: <ResourceRecordSets: Z6Q71ND65H5MS>
g - conn.get_all_rrsets(hosted_zone_id="Z6Q71ND65H5MS")
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: TypeError: unsupported operand type(s) for -: 'Route53Connection' and 'ResourceRecordSets'
sets =  conn.get_all_rrsets(hosted_zone_id="Z6Q71ND65H5MS")
rset = setes.next()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: NameError: name 'setes' is not defined
rset = sets.next()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: AttributeError: 'ResourceRecordSets' object has no attribute 'next'
sets
# OUT: <ResourceRecordSets: Z6Q71ND65H5MS>
rset = [x for x in sets]
rset
# OUT: [<boto.route53.record.Record object at 0x10a575650>, <boto.route53.record.Record object at 0x10a5756d0>, <boto.route53.record.Record object at 0x10a575310>]
rset[0]
# OUT: <boto.route53.record.Record object at 0x10a575650>
rset[0].name
# OUT: u'laironald.com.'
rset[0].type
# OUT: u'NS'
rr = rset[0]
rr.identifier
rr.XMLBody
# OUT: '<ResourceRecordSet>\n        <Name>%(name)s</Name>\n        <Type>%(type)s</Type>\n        %(weight)s\n        %(body)s\n    </ResourceRecordSet>'
rr.ttl
# OUT: u'172800'
rr.weight
rr.AliasBody
# OUT: '<AliasTarget>\n        <HostedZoneId>%s</HostedZoneId>\n        <DNSName>%s</DNSName>\n    </AliasTarget>'
rr.ResourceRecordBody
# OUT: '<ResourceRecord>\n        <Value>%s</Value>\n    </ResourceRecord>'
rr.WRRBody
# OUT: '\n        <SetIdentifier>%(identifier)s</SetIdentifier>\n        <Weight>%(weight)s</Weight>\n    '
rr.to_print
# OUT: <bound method Record.to_print of <boto.route53.record.Record object at 0x10a575650>>
rr.name
# OUT: u'laironald.com.'
rr.resource_records
# OUT: [u'ns-1545.awsdns-01.co.uk.', u'ns-1358.awsdns-41.org.', u'ns-397.awsdns-49.com.', u'ns-694.awsdns-22.net.']
rr2 = rset[1]
rr2.name
# OUT: u'laironald.com.'
rr2.resource_records
# OUT: [u'ns-1545.awsdns-01.co.uk. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400']
rr2 = rset[2]
rr2.resource_records
# OUT: [u'173.255.244.139']
rr2.resource_records = ['1.1.1.1']
rr2.resource_records
# OUT: ['1.1.1.1']
host
# OUT: {u'GetHostedZoneResponse': {u'HostedZone': {u'CallerReference': u'7A107689-F884-E1D4-B1E1-E91AB2F426FB', u'Config': {}, u'Id': u'/hostedzone/Z6Q71ND65H5MS', u'Name': u'laironald.com.'}, u'DelegationSet': {u'NameServers': [u'ns-1545.awsdns-01.co.uk', u'ns-1358.awsdns-41.org', u'ns-397.awsdns-49.com', u'ns-694.awsdns-22.net']}}}
rr2.to_xml()
# OUT: u'<ResourceRecordSet>\n        <Name>test.laironald.com.</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>300</TTL>\n        <ResourceRecords>\n            <ResourceRecord>\n        <Value>1.1.1.1</Value>\n    </ResourceRecord>\n        </ResourceRecords>\n    </ResourceRecordSet>'
changes.add_change(action="CREATE", name="laironald.com", type="A")
# OUT: <boto.route53.record.Record object at 0x10a551b10>
rr_xml = rr2.to_xml()
rr_xml
# OUT: u'<ResourceRecordSet>\n        <Name>test.laironald.com.</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>300</TTL>\n        <ResourceRecords>\n            <ResourceRecord>\n        <Value>1.1.1.1</Value>\n    </ResourceRecord>\n        </ResourceRecords>\n    </ResourceRecordSet>'
print rr_xml
# OUT: <ResourceRecordSet>
# OUT:         <Name>test.laironald.com.</Name>
# OUT:         <Type>A</Type>
# OUT:         <TTL>300</TTL>
# OUT:         <ResourceRecords>
# OUT:             <ResourceRecord>
# OUT:         <Value>1.1.1.1</Value>
# OUT:     </ResourceRecord>
# OUT:         </ResourceRecords>
# OUT:     </ResourceRecordSet>
resp = conn.change_rrsets("Z6Q71ND65H5MS", xml_body=rr2.to_xml())
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/connection.py", line 291, in change_rrsets
# OUT:     body)
# OUT: DNSServerError: DNSServerError: 400 Bad Request
# OUT: <?xml version="1.0"?>
# OUT: <ErrorResponse xmlns="https://route53.amazonaws.com/doc/2011-05-05/"><Error><Type>Sender</Type><Code>MalformedInput</Code><Message>ResourceRecordSet is not valid, expected ChangeResourceRecordSetsRequest</Message></Error><RequestId>eb1d47e4-c630-11e1-b59b-c791621f18ac</RequestId></ErrorResponse>
rr2.alias_dns_name
rr2.alias_dns_name()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: TypeError: 'NoneType' object is not callable
print rr2.name
# OUT: test.laironald.com.
xml = "<?xml version="1.0" encoding="UTF-8"?>
# OUT:   File "<input>", line 1
# OUT:     xml = "<?xml version="1.0" encoding="UTF-8"?>
# OUT:                             ^
# OUT: SyntaxError: invalid syntax
    <ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2010-10-01/">
# OUT:   File "<input>", line 2
# OUT:     <ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2010-10-01/">
# OUT:    ^
# OUT: IndentationError: unexpected indent
        <ChangeBatch>
# OUT:   File "<input>", line 2
# OUT:     <ChangeBatch>
# OUT:    ^
# OUT: IndentationError: unexpected indent
            <Comment>Add record</Comment>
# OUT:   File "<input>", line 2
# OUT:     <Comment>Add record</Comment>
# OUT:    ^
# OUT: IndentationError: unexpected indent
            <Changes>
# OUT:   File "<input>", line 2
# OUT:     <Changes>
# OUT:    ^
# OUT: IndentationError: unexpected indent
                <Change>
# OUT:   File "<input>", line 2
# OUT:     <Change>
# OUT:    ^
# OUT: IndentationError: unexpected indent
                    <Action>CREATE</Action>
# OUT:   File "<input>", line 2
# OUT:     <Action>CREATE</Action>
# OUT:    ^
# OUT: IndentationError: unexpected indent
xml = """<?xml version="1.0" encoding="UTF-8"?>
    <ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2010-10-01/">
        <ChangeBatch>
            <Comment>Add record</Comment>
            <Changes>
                <Change>
                    <Action>CREATE</Action>{RRS}</Change></Changes></ChangeBatch></ChangeResourceRecordSetsRequest>"""
resp = conn.change_rrsets(Z6Q71ND65H5MS, xml.format(RRS=rr_xml))
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: NameError: name 'Z6Q71ND65H5MS' is not defined
resp = conn.change_rrsets("Z6Q71ND65H5MS", xml.format(RRS=rr_xml))
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/connection.py", line 291, in change_rrsets
# OUT:     body)
# OUT: DNSServerError: DNSServerError: 400 Bad Request
# OUT: <?xml version="1.0"?>
# OUT: <ErrorResponse xmlns="https://route53.amazonaws.com/doc/2011-05-05/"><Error><Type>Sender</Type><Code>InvalidInput</Code><Message>Invalid XML ; cvc-elt.1: Cannot find the declaration of element 'ChangeResourceRecordSetsRequest'.</Message></Error><RequestId>7990b888-c631-11e1-b59b-c791621f18ac</RequestId></ErrorResponse>
xml.format(RRS=rr_xml)
# OUT: '<?xml version="1.0" encoding="UTF-8"?>\n    <ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2010-10-01/">\n        <ChangeBatch>\n            <Comment>Add record</Comment>\n            <Changes>\n                <Change>\n                    <Action>CREATE</Action><ResourceRecordSet>\n        <Name>test.laironald.com.</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>300</TTL>\n        <ResourceRecords>\n            <ResourceRecord>\n        <Value>1.1.1.1</Value>\n    </ResourceRecord>\n        </ResourceRecords>\n    </ResourceRecordSet></Change></Changes></ChangeBatch></ChangeResourceRecordSetsRequest>'
print xml.format(RRS=rr_xml)
# OUT: <?xml version="1.0" encoding="UTF-8"?>
# OUT:     <ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2010-10-01/">
# OUT:         <ChangeBatch>
# OUT:             <Comment>Add record</Comment>
# OUT:             <Changes>
# OUT:                 <Change>
# OUT:                     <Action>CREATE</Action><ResourceRecordSet>
# OUT:         <Name>test.laironald.com.</Name>
# OUT:         <Type>A</Type>
# OUT:         <TTL>300</TTL>
# OUT:         <ResourceRecords>
# OUT:             <ResourceRecord>
# OUT:         <Value>1.1.1.1</Value>
# OUT:     </ResourceRecord>
# OUT:         </ResourceRecords>
# OUT:     </ResourceRecordSet></Change></Changes></ChangeBatch></ChangeResourceRecordSetsRequest>
changes.add_change(action="CREATE", name="laironald.com", type="A")
# OUT: <boto.route53.record.Record object at 0x10a56d810>
changes.add_value("123.12.21.12")
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: AttributeError: 'ResourceRecordSets' object has no attribute 'add_value'
change = changes.add_change(action="CREATE", name="laironald.com", type="A")
change.add_value("1.1.1.1")
changees.commit()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: NameError: name 'changees' is not defined
changes.commit()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/record.py", line 131, in commit
# OUT:     return self.connection.change_rrsets(self.hosted_zone_id, self.to_xml())
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/connection.py", line 291, in change_rrsets
# OUT:     body)
# OUT: DNSServerError: DNSServerError: 400 Bad Request
# OUT: <?xml version="1.0"?>
# OUT: <ErrorResponse xmlns="https://route53.amazonaws.com/doc/2011-05-05/"><Error><Type>Sender</Type><Code>MalformedInput</Code><Message>Unexpected list element termination</Message></Error><RequestId>298fcdd7-c632-11e1-b6e7-c71694ebc5fa</RequestId></ErrorResponse>
print change.to_xml()
# OUT: <ResourceRecordSet>
# OUT:         <Name>laironald.com</Name>
# OUT:         <Type>A</Type>
# OUT:         <TTL>600</TTL>
# OUT:         <ResourceRecords>
# OUT:             <ResourceRecord>
# OUT:         <Value>1.1.1.1</Value>
# OUT:     </ResourceRecord>
# OUT:         </ResourceRecords>
# OUT:     </ResourceRecordSet>
print rr_xml
# OUT: <ResourceRecordSet>
# OUT:         <Name>test.laironald.com.</Name>
# OUT:         <Type>A</Type>
# OUT:         <TTL>300</TTL>
# OUT:         <ResourceRecords>
# OUT:             <ResourceRecord>
# OUT:         <Value>1.1.1.1</Value>
# OUT:     </ResourceRecord>
# OUT:         </ResourceRecords>
# OUT:     </ResourceRecordSet>
changes.commit()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/record.py", line 131, in commit
# OUT:     return self.connection.change_rrsets(self.hosted_zone_id, self.to_xml())
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/connection.py", line 291, in change_rrsets
# OUT:     body)
# OUT: DNSServerError: DNSServerError: 400 Bad Request
# OUT: <?xml version="1.0"?>
# OUT: <ErrorResponse xmlns="https://route53.amazonaws.com/doc/2011-05-05/"><Error><Type>Sender</Type><Code>MalformedInput</Code><Message>Unexpected list element termination</Message></Error><RequestId>60d658b0-c632-11e1-9014-0f1dc8a6d2ee</RequestId></ErrorResponse>
changes
# OUT: <ResourceRecordSets: Z6Q71ND65H5MS>
change = changes.add_change(action="CREATE", name="blah.laironald.com", type="A")
change.add_value("1.1.1.1")
changes.commit()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/record.py", line 131, in commit
# OUT:     return self.connection.change_rrsets(self.hosted_zone_id, self.to_xml())
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/connection.py", line 291, in change_rrsets
# OUT:     body)
# OUT: DNSServerError: DNSServerError: 400 Bad Request
# OUT: <?xml version="1.0"?>
# OUT: <ErrorResponse xmlns="https://route53.amazonaws.com/doc/2011-05-05/"><Error><Type>Sender</Type><Code>MalformedInput</Code><Message>Unexpected list element termination</Message></Error><RequestId>8ae1706f-c632-11e1-9014-0f1dc8a6d2ee</RequestId></ErrorResponse>
changes.hosted_zone_id
# OUT: 'Z6Q71ND65H5MS'
changes.to_xml()
# OUT: '<?xml version="1.0" encoding="UTF-8"?>\n    <ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2011-05-05/">\n            <ChangeBatch>\n                <Comment>None</Comment>\n                <Changes><Change>\n        <Action>CREATE</Action>\n        <ResourceRecordSet>\n        <Name>laironald.com</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>600</TTL>\n        <ResourceRecords>\n            \n        </ResourceRecords>\n    </ResourceRecordSet>\n    </Change><Change>\n        <Action>CREATE</Action>\n        <ResourceRecordSet>\n        <Name>laironald.com</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>600</TTL>\n        <ResourceRecords>\n            \n        </ResourceRecords>\n    </ResourceRecordSet>\n    </Change><Change>\n        <Action>CREATE</Action>\n        <ResourceRecordSet>\n        <Name>laironald.com</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>600</TTL>\n        <ResourceRecords>\n            \n        </ResourceRecords>\n    </ResourceRecordSet>\n    </Change><Change>\n        <Action>CREATE</Action>\n        <ResourceRecordSet>\n        <Name>laironald.com</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>600</TTL>\n        <ResourceRecords>\n            <ResourceRecord>\n        <Value>1.1.1.1</Value>\n    </ResourceRecord>\n        </ResourceRecords>\n    </ResourceRecordSet>\n    </Change><Change>\n        <Action>CREATE</Action>\n        <ResourceRecordSet>\n        <Name>blah.laironald.com</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>600</TTL>\n        <ResourceRecords>\n            <ResourceRecord>\n        <Value>1.1.1.1</Value>\n    </ResourceRecord>\n        </ResourceRecords>\n    </ResourceRecordSet>\n    </Change></Changes>\n            </ChangeBatch>\n        </ChangeResourceRecordSetsRequest>'
print changes.to_xml()
# OUT: <?xml version="1.0" encoding="UTF-8"?>
# OUT:     <ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2011-05-05/">
# OUT:             <ChangeBatch>
# OUT:                 <Comment>None</Comment>
# OUT:                 <Changes><Change>
# OUT:         <Action>CREATE</Action>
# OUT:         <ResourceRecordSet>
# OUT:         <Name>laironald.com</Name>
# OUT:         <Type>A</Type>
# OUT:         <TTL>600</TTL>
# OUT:         <ResourceRecords>
# OUT:         </ResourceRecords>
# OUT:     </ResourceRecordSet>
# OUT:     </Change><Change>
# OUT:         <Action>CREATE</Action>
# OUT:         <ResourceRecordSet>
# OUT:         <Name>laironald.com</Name>
# OUT:         <Type>A</Type>
# OUT:         <TTL>600</TTL>
# OUT:         <ResourceRecords>
# OUT:         </ResourceRecords>
# OUT:     </ResourceRecordSet>
# OUT:     </Change><Change>
# OUT:         <Action>CREATE</Action>
# OUT:         <ResourceRecordSet>
# OUT:         <Name>laironald.com</Name>
# OUT:         <Type>A</Type>
# OUT:         <TTL>600</TTL>
# OUT:         <ResourceRecords>
# OUT:         </ResourceRecords>
# OUT:     </ResourceRecordSet>
# OUT:     </Change><Change>
# OUT:         <Action>CREATE</Action>
# OUT:         <ResourceRecordSet>
# OUT:         <Name>laironald.com</Name>
# OUT:         <Type>A</Type>
# OUT:         <TTL>600</TTL>
# OUT:         <ResourceRecords>
# OUT:             <ResourceRecord>
# OUT:         <Value>1.1.1.1</Value>
# OUT:     </ResourceRecord>
# OUT:         </ResourceRecords>
# OUT:     </ResourceRecordSet>
# OUT:     </Change><Change>
# OUT:         <Action>CREATE</Action>
# OUT:         <ResourceRecordSet>
# OUT:         <Name>blah.laironald.com</Name>
# OUT:         <Type>A</Type>
# OUT:         <TTL>600</TTL>
# OUT:         <ResourceRecords>
# OUT:             <ResourceRecord>
# OUT:         <Value>1.1.1.1</Value>
# OUT:     </ResourceRecord>
# OUT:         </ResourceRecords>
# OUT:     </ResourceRecordSet>
# OUT:     </Change></Changes>
# OUT:             </ChangeBatch>
# OUT:         </ChangeResourceRecordSetsRequest>
changes.to_xml()
# OUT: '<?xml version="1.0" encoding="UTF-8"?>\n    <ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2011-05-05/">\n            <ChangeBatch>\n                <Comment>None</Comment>\n                <Changes><Change>\n        <Action>CREATE</Action>\n        <ResourceRecordSet>\n        <Name>laironald.com</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>600</TTL>\n        <ResourceRecords>\n            \n        </ResourceRecords>\n    </ResourceRecordSet>\n    </Change><Change>\n        <Action>CREATE</Action>\n        <ResourceRecordSet>\n        <Name>laironald.com</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>600</TTL>\n        <ResourceRecords>\n            \n        </ResourceRecords>\n    </ResourceRecordSet>\n    </Change><Change>\n        <Action>CREATE</Action>\n        <ResourceRecordSet>\n        <Name>laironald.com</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>600</TTL>\n        <ResourceRecords>\n            \n        </ResourceRecords>\n    </ResourceRecordSet>\n    </Change><Change>\n        <Action>CREATE</Action>\n        <ResourceRecordSet>\n        <Name>laironald.com</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>600</TTL>\n        <ResourceRecords>\n            <ResourceRecord>\n        <Value>1.1.1.1</Value>\n    </ResourceRecord>\n        </ResourceRecords>\n    </ResourceRecordSet>\n    </Change><Change>\n        <Action>CREATE</Action>\n        <ResourceRecordSet>\n        <Name>blah.laironald.com</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>600</TTL>\n        <ResourceRecords>\n            <ResourceRecord>\n        <Value>1.1.1.1</Value>\n    </ResourceRecord>\n        </ResourceRecords>\n    </ResourceRecordSet>\n    </Change></Changes>\n            </ChangeBatch>\n        </ChangeResourceRecordSetsRequest>'
changes = conn.get_all_rrsets(changes.hosted_zone_id)
changes.hosted_zone_id
# OUT: 'Z6Q71ND65H5MS'
change = changes.add_change(action="CREATE", name="blah.laironald.com", type="A")
change.add_value("HELLO!")
change.add_value("1.2.2.3")
changes.commit()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/record.py", line 131, in commit
# OUT:     return self.connection.change_rrsets(self.hosted_zone_id, self.to_xml())
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/connection.py", line 291, in change_rrsets
# OUT:     body)
# OUT: DNSServerError: DNSServerError: 400 Bad Request
# OUT: <?xml version="1.0"?>
# OUT: <ErrorResponse xmlns="https://route53.amazonaws.com/doc/2011-05-05/"><Error><Type>Sender</Type><Code>InvalidChangeBatch</Code><Message>Invalid Resource Record: FATAL problem: ARRDATAIllegalIPv4Address encountered at HELLO!</Message></Error><RequestId>f7fb2038-c632-11e1-9014-0f1dc8a6d2ee</RequestId></ErrorResponse>
changes = conn.get_all_rrsets(changes.hosted_zone_id)
change = changes.add_change(action="CREATE", name="blah.laironald.com", type="A")
change.add_value("1.2.2.3")
changes.commit()
# OUT: {u'ChangeResourceRecordSetsResponse': {u'ChangeInfo': {u'Status': u'PENDING', u'SubmittedAt': u'2012-07-04T23:50:17.662Z', u'Id': u'/change/C7DG2VSY1T1YG'}}}
change = changes.add_change(action="CREATE", name="blah.laironald.com", type="A")
change.add_value("1.2.2.5")
changes.commit()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/record.py", line 131, in commit
# OUT:     return self.connection.change_rrsets(self.hosted_zone_id, self.to_xml())
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/connection.py", line 291, in change_rrsets
# OUT:     body)
# OUT: DNSServerError: DNSServerError: 400 Bad Request
# OUT: <?xml version="1.0"?>
# OUT: <ErrorResponse xmlns="https://route53.amazonaws.com/doc/2011-05-05/"><Error><Type>Sender</Type><Code>InvalidChangeBatch</Code><Message>Tried to create resource record set blah.laironald.com., type A but it already exists</Message></Error><RequestId>126ed2f7-c633-11e1-9014-0f1dc8a6d2ee</RequestId></ErrorResponse>
change = changes.add_change(action="DELETE", name="blah.laironald.com", type="A")
changes.commit()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/record.py", line 131, in commit
# OUT:     return self.connection.change_rrsets(self.hosted_zone_id, self.to_xml())
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/connection.py", line 291, in change_rrsets
# OUT:     body)
# OUT: DNSServerError: DNSServerError: 400 Bad Request
# OUT: <?xml version="1.0"?>
# OUT: <ErrorResponse xmlns="https://route53.amazonaws.com/doc/2011-05-05/"><Error><Type>Sender</Type><Code>MalformedInput</Code><Message>Unexpected list element termination</Message></Error><RequestId>1dc86703-c633-11e1-9f61-b9301fd90224</RequestId></ErrorResponse>
print changes.to_xml()
# OUT: <?xml version="1.0" encoding="UTF-8"?>
# OUT:     <ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2011-05-05/">
# OUT:             <ChangeBatch>
# OUT:                 <Comment>None</Comment>
# OUT:                 <Changes><Change>
# OUT:         <Action>CREATE</Action>
# OUT:         <ResourceRecordSet>
# OUT:         <Name>blah.laironald.com</Name>
# OUT:         <Type>A</Type>
# OUT:         <TTL>600</TTL>
# OUT:         <ResourceRecords>
# OUT:             <ResourceRecord>
# OUT:         <Value>1.2.2.3</Value>
# OUT:     </ResourceRecord>
# OUT:         </ResourceRecords>
# OUT:     </ResourceRecordSet>
# OUT:     </Change><Change>
# OUT:         <Action>CREATE</Action>
# OUT:         <ResourceRecordSet>
# OUT:         <Name>blah.laironald.com</Name>
# OUT:         <Type>A</Type>
# OUT:         <TTL>600</TTL>
# OUT:         <ResourceRecords>
# OUT:             <ResourceRecord>
# OUT:         <Value>1.2.2.5</Value>
# OUT:     </ResourceRecord>
# OUT:         </ResourceRecords>
# OUT:     </ResourceRecordSet>
# OUT:     </Change><Change>
# OUT:         <Action>DELETE</Action>
# OUT:         <ResourceRecordSet>
# OUT:         <Name>blah.laironald.com</Name>
# OUT:         <Type>A</Type>
# OUT:         <TTL>600</TTL>
# OUT:         <ResourceRecords>
# OUT:         </ResourceRecords>
# OUT:     </ResourceRecordSet>
# OUT:     </Change></Changes>
# OUT:             </ChangeBatch>
# OUT:         </ChangeResourceRecordSetsRequest>
changes = conn.get_all_rrsets(changes.hosted_zone_id)
change = changes.add_change(action="DELETE", name="blah.laironald.com", type="A")
changes.commit()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/record.py", line 131, in commit
# OUT:     return self.connection.change_rrsets(self.hosted_zone_id, self.to_xml())
# OUT:   File "/Library/Python/2.7/site-packages/boto/route53/connection.py", line 291, in change_rrsets
# OUT:     body)
# OUT: DNSServerError: DNSServerError: 400 Bad Request
# OUT: <?xml version="1.0"?>
# OUT: <ErrorResponse xmlns="https://route53.amazonaws.com/doc/2011-05-05/"><Error><Type>Sender</Type><Code>MalformedInput</Code><Message>Unexpected list element termination</Message></Error><RequestId>346b6307-c633-11e1-9f61-b9301fd90224</RequestId></ErrorResponse>
print changes.to_xml()
# OUT: <?xml version="1.0" encoding="UTF-8"?>
# OUT:     <ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2011-05-05/">
# OUT:             <ChangeBatch>
# OUT:                 <Comment>None</Comment>
# OUT:                 <Changes><Change>
# OUT:         <Action>DELETE</Action>
# OUT:         <ResourceRecordSet>
# OUT:         <Name>blah.laironald.com</Name>
# OUT:         <Type>A</Type>
# OUT:         <TTL>600</TTL>
# OUT:         <ResourceRecords>
# OUT:         </ResourceRecords>
# OUT:     </ResourceRecordSet>
# OUT:     </Change></Changes>
# OUT:             </ChangeBatch>
# OUT:         </ChangeResourceRecordSetsRequest>
changes = conn.get_all_rrsets(changes.hosted_zone_id)
change = changes.add_change(action="DELETE", name="blah.laironald.com")
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: TypeError: add_change() takes at least 4 arguments (3 given)
change = changes.add_change(action="DELETE", name="blah.laironald.com", type="A")
change.to_xml()
# OUT: '<ResourceRecordSet>\n        <Name>blah.laironald.com</Name>\n        <Type>A</Type>\n        \n        \n        <TTL>600</TTL>\n        <ResourceRecords>\n            \n        </ResourceRecords>\n    </ResourceRecordSet>'
change.add_value("1.2.2.3")
changes.commit()
# OUT: {u'ChangeResourceRecordSetsResponse': {u'ChangeInfo': {u'Status': u'PENDING', u'SubmittedAt': u'2012-07-04T23:54:08.646Z', u'Id': u'/change/C1FZTUD4I1B6ZN'}}}
