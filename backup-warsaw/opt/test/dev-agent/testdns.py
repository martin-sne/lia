#!/usr/bin/env python
import dns.resolver
import dns.zone
import dns.rdtypes.ANY
import re

totalrrsig=0


def get_rrsig_recordcount():
        zone = dns.zone.from_xfr(dns.query.xfr('145.100.104.165', 'derby.practicum.os3.nl'))
	names = zone.nodes.keys()
        names.sort()

	rrsig=[]
        for rr in names:
		rrsig.append(re.findall(r'.*IN\s+RRSIG.*',zone[rr].to_text(rr)))
		
	return len(rrsig)

rrsigcount = get_rrsig_recordcount()
print rrsigcount

