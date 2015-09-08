#!/usr/bin/env python
import sys
import dns.query
import dns.zone
import dns.rdatatype
import dns.resolver
import dns.name
import dns.message
import Crypto

# TODO Make it generic for a list of domains
# split into functios
# get SOA TTL
# get Minimum TTL
# get SOA Record 
# dig  warsaw.practicum.os3.nl. dnskey | grep 257 | dnssec-dsfromkey -f /dev/stdin warsaw.practicum.os3.nl. | tail -n 1 
# rename  dnssecZoneGlobalDSValidated to  dnssecZoneGlobalDSMatchesDNSKEY
#  dnssecZoneGlobalDSSignatureVerification 
#  dnssecZoneGlobalRRSigning
#  dnssecZoneGlobalDNSKEYSignatureVerification 

domain = 'paris.derby.practicum.os3.nl'

# get all data 
z = dns.zone.from_xfr(dns.query.xfr('145.100.104.62', 'paris.derby.practicum.os3.nl'))

# get  dnssecZoneGlobalOrigin
print "Zone origin:", z.origin


# get  dnssecZoneGlobalRecordSetCount and dnssecZoneGlobalRecordCount
names = z.nodes.keys()
names.sort()

totalrecordsets = 0
totalrecords = 0
for rr in names:
    totalrecordsets += len(rr)	
    #print z[rr].to_text(rr)
    raw = z[rr].to_text(rr) 
    lines = raw.split('\n') 
    totalrecords += len(lines)
    #print "Lines", lines
    #print lines[1]
 
print "Total Recordsets:", totalrecordsets
print "Total Records:", totalrecords

# get delegation count

z = dns.zone.from_xfr(dns.query.xfr('145.100.104.62', 'paris.derby.practicum.os3.nl'))
totaldelegations = 0
for (name, rdataset) in z.iterate_rdatasets(dns.rdatatype.NS):
        if name != dns.name.empty:
                totaldelegations += len(rdataset)
		#print rdataset
		#print name
print "Total delegations:", totaldelegations

def get_authoritative_nameserver(domain, log=lambda msg: None):
    global nameserver
    n = dns.name.from_text(domain)

    depth = 5
    default = dns.resolver.get_default_resolver()
    nameserver = default.nameservers[0]

    last = False
    while not last:
        s = n.split(depth)

        last = s[0].to_unicode() == u'@'
        sub = s[1]

        log('Looking up %s on %s' % (sub, nameserver))
        query = dns.message.make_query(sub, dns.rdatatype.NS)
        response = dns.query.udp(query, nameserver)

        rcode = response.rcode()
        if rcode != dns.rcode.NOERROR:
            if rcode == dns.rcode.NXDOMAIN:
                raise Exception('%s does not exist.' % sub)
            else:
                raise Exception('Error %s' % dns.rcode.to_text(rcode))

        rrset = None
        if len(response.authority) > 0:
            rrset = response.authority[0]
        else:
            rrset = response.answer[0]

        rr = rrset[0]
        if rr.rdtype == dns.rdatatype.SOA:
            log('Same server is authoritative for %s' % sub)
        else:
            authority = rr.target
            log('%s is authoritative for %s' % (authority, sub))
            nameserver = default.query(authority).rrset[0].to_text()

        depth += 1

    #return nameserver



def log(msg):
    print msg

#print get_authoritative_nameserver(domain, log)
#domain = 'surfnet.nl'

get_authoritative_nameserver(domain, log)

# get Authnsserver

totalns = 0
#domain = 'warsaw.practicum.os3.nl'
response = dns.resolver.query(domain,'NS')
for server in response:
    print server
    totalns += 1
print "Total authoritative NS:", totalns    


# Validation
# we'll use the first nameserver in this example
# get DNSKEY for zone

request = dns.message.make_query(domain,
                                 dns.rdatatype.DNSKEY,
                                 want_dnssec=True)

response = dns.query.udp(request,nameserver)
answer = response.answer
name = dns.name.from_text(domain)
print answer

try:
    dns.dnssec.validate(answer[0],answer[1],{name:answer[0]})
except dns.dnssec.ValidationFailure:
# BE SUSPICIOUS
    print "NOK VAL"
else:
# WE'RE GOOD, THERE'S A VALID DNSSEC SELF-SIGNED KEY FOR example.com
    print "Validation succeed for DNSKEY of Zone", domain, " by querying nameserver with IP ", nameserver,  


