#!/usr/bin/env python
import sys
import dns.query
import dns.zone
import dns.rdatatype
import dns.resolver
import dns.name
import dns.message
import Crypto
import re

domains = { 'warsaw.practicum.os3.nl' : '1',
            'paris.derby.practicum.os3.nl' : '2',
        }

#domain="warsaw.practicum.os3.nl"

def get_authoritative_nameserver_ip(domain, log=lambda msg: None):
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

    return nameserver

def log(msg):
    print msg

def get_authoritative_nameserver(domain):
    answers = dns.resolver.query(domain, 'NS')
    global ns
    ns = []
    for rdata in answers:
    	n = str(rdata)
    	ns.append(n)
    return ns


def get_zone_xfr(domain,nameserver):
    global zone
    zone = dns.zone.from_xfr(dns.query.xfr(nameserver, domain))
    names = zone.nodes.keys()
    names.sort()

    for rr in names:
        raw = zone[rr].to_text(rr)
        lines = raw.split('\n')
    	return raw

def get_origin_recordcount(domain,nameserver):
	# TODO: Implement in a way, that only one XFR is required
	zone = dns.zone.from_xfr(dns.query.xfr(nameserver, domain))
    	names = zone.nodes.keys()
    	names.sort()

    	totalrecordsets = 0
    	totalrecords = 0
	for rr in names:
        	totalrecordsets += len(rr)
        	raw = zone[rr].to_text(rr)
		lines = raw.split('\n')
        	totalrecords += len(lines)
	
	totaldelegations = 0
    	for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.NS):
        	if name != dns.name.empty:
                	totaldelegations += len(rdataset)
	
	print "Total Recordsets:", totalrecordsets
        print "Total Records:", totalrecords
        print "Zone origin:", zone.origin
        print "Total delegations:", totaldelegations


def validate_dnskey(domain,nameserver):
    request = dns.message.make_query(domain,
                                 dns.rdatatype.DNSKEY,
                                 want_dnssec=True)

    response = dns.query.udp(request,nameserver)

    if response.rcode() != 0:
	return None

    answer = response.answer
    name = dns.name.from_text(domain)
    print answer

    try:
        dns.dnssec.validate(answer[0],answer[1],{name:answer[0]})
    except dns.dnssec.ValidationFailure:
        print "NOK VAL"
    else:
    # WE'RE GOOD, THERE'S A VALID DNSSEC SELF-SIGNED KEY FOR example.com
        print "Validation succeed for DNSKEY of Zone", domain, " by querying nameserver with IP ", nameserver, 


def get_soa(domain,nameserver):
    request = dns.message.make_query(domain,
                                 dns.rdatatype.SOA)

    response = dns.query.udp(request,nameserver)
    print "SOA Record", response.answer[0]
    #print response.additional[0]
    #print response.authority[0]
    soa = str(response.answer[0])
    soa_parts = soa.split()
    print "SOA TTL", soa_parts[1]

def minimum_ttl(domain,nameserver):
	data=get_zone_xfr(domain,nameserver)
	#print data
	minimum_ttl=re.findall(r'.*IN.*',data)
	#print minimum_ttl
	minimum_ttl_list = []
	for values in minimum_ttl:
		values_list=values.split()
		if values_list[1] == '0':
			continue
		else:
                	minimum_ttl_list.append(values_list[1])
		#print values_list[1]
	print "Minimum TTL", min(minimum_ttl_list)

for domain in sorted(domains.iterkeys()):

	get_authoritative_nameserver_ip(domain, log)
	print "IP address of nameser: ", nameserver

	get_authoritative_nameserver(domain)
	print "Namservers", ns
	print "Namservercount", len(ns)

	get_zone_xfr(domain,nameserver)
	get_soa(domain,nameserver)

	validate_dnskey(domain,nameserver)
	minimum_ttl(domain,nameserver)
	get_origin_recordcount(domain,nameserver)
