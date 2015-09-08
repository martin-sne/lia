#!/usr/bin/env python
import dns.query
import dns.zone
import dns.rdatatype
import dns.resolver
import dns.name
import dns.message
import re

global nameserver 
nameserver = '145.100.104.165'

def get_all_authoritative_nameservers():
    request_ns = dns.message.make_query('berlin.warsaw.practicum.os3.nl',
                                 dns.rdatatype.NS)

    response_ns = dns.query.udp(request_ns,nameserver)
    ns = []	

    for rdata in response_ns.answer:		
	ns_name = re.split('\s+',str(rdata))
	ns_data = ' '.join(ns_name)
	ns = re.findall(r"(?<=NS\s)(\b[A-Za-z0-9.-_]*\b)", ns_data)		
	 
    return ns, len(ns)

get_all_authserver = get_all_authoritative_nameservers()

nameserverlist = ' '.join(get_all_authserver[0])
print nameserverlist 
print get_all_authserver[1]

def get_origin_recordcount():
        # TODO: Implement in a way, that only one XFR is required
        zone = dns.zone.from_xfr(dns.query.xfr(nameserver, 'berlin.warsaw.practicum.os3.nl'))
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
	totalds = 0
	for (name, rdataset) in zone.iterate_rdatasets(dns.rdatatype.DS):
                if name != dns.name.empty:
                        totalds += len(rdataset)
	if totalds == totaldelegations:
		ds_present_match = 1		
	else:
		ds_present_match = 2

        return zone.origin, totalrecords, totalrecordsets, totaldelegations, ds_present_match

test = get_origin_recordcount()
print test
