#!/usr/bin/env python

import dns.resolver

domain = 'google.com'
answers = dns.resolver.query(domain,'NS')
for server in answers:
    print server
