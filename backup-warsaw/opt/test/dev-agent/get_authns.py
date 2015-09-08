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

global domains

domains = { 'warsaw.practicum.os3.nl' : '1',
            'paris.derby.practicum.os3.nl' : '2',
          }

#domain="warsaw.practicum.os3.nl"

def get_authoritative_nameserver_ip():
   global nameserver
   n = dns.name.from_text(domain)

   default = dns.resolver.get_default_resolver()
   nameserver = default.nameservers[0]

   #log('Looking up %s on %s' % (domain, nameserver))
   query = dns.message.make_query(domain, dns.rdatatype.NS)
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
   authority = rr.target
   #log('%s is authoritative for %s' % (authority, domain))
   nameserver = default.query(authority).rrset[0].to_text()

   return nameserver,authority,domain

def log(msg):
    print msg

for domain in sorted(domains.iterkeys()):

	test = get_authoritative_nameserver_ip()
        print "IP address  : ", test[0]
	print "authority: ", test[1]
	print "domain: ", test[2]
