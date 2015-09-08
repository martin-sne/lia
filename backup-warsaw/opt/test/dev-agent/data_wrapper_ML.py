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
import xml.etree.cElementTree as ET

global domains
global nameserver
global xmlfeed

xmlfeed={}

domains = { 'warsaw.practicum.os3.nl' : '1',
	    'paris.derby.practicum.os3.nl' : '2',
	    'derby.practicum.os3.nl' : '3',
	    'berlin.warsaw.practicum.os3.nl' : 4			
        }


def get_authoritative_nameserver_data():
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

def get_all_authoritative_nameservers():
    answers = dns.resolver.query(domain, 'NS')
    ns = []
    for rdata in answers:
    	n = str(rdata)
    	ns.append(n)
    return ns,len(ns)


def get_zone_xfr(domain,nameserver):
    global zone
    zone = dns.zone.from_xfr(dns.query.xfr(nameserver, domain))
    names = zone.nodes.keys()
    names.sort()

    for rr in names:
        raw = zone[rr].to_text(rr)
        lines = raw.split('\n')
    	return raw

def get_origin_recordcount():
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
	
	return zone.origin, totalrecords, totalrecordsets, totaldelegations

def validate_dnskey():
    ret_val = 3
    request = dns.message.make_query(domain,
                                 dns.rdatatype.DNSKEY,
                                 want_dnssec=True)

    response = dns.query.udp(request,nameserver)

    if response.rcode() != 0:
	ret_val = 3
	return ret_val

    answer = response.answer
    name = dns.name.from_text(domain)

    try:
        dns.dnssec.validate(answer[0],answer[1],{name:answer[0]})
    except dns.dnssec.ValidationFailure:
    	pass
    else:
    # valid DNSSEC selfsigned DNSKEY for domain
	ret_val = 1
	return ret_val

def get_soa():
    request = dns.message.make_query(domain,
                                 dns.rdatatype.SOA)

    response = dns.query.udp(request,nameserver)
    soa = str(response.answer[0])
    soa_parts = soa.split()
    return response.answer[0],soa_parts[1]

def minimum_ttl():
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
	return min(minimum_ttl_list)


# Update XML template with retrived values
def editXML():  
	filename='updated.xml'      
        global xmlfeed
        tree = ET.ElementTree(file=filename)
        root = tree.getroot()

        # get all zones
        for child_of_root in root:
                zones = child_of_root.attrib

                # build path for xpath query
                # Example: 'Zone[@name="os3.nl"]/table'
                path = "Zone[@name=\"" + zones['name'] + "\"]/table" 
                # get all tables 
                for table in tree.iterfind(path):
                        tables=table.attrib

                        # build path for xpath query 
                        # Example: 'Zone[@name="os3.nl"]/table[@name="dnssecGlobalZoneTable"]/item/data' 
                        path2= "Zone[@name=\"" + zones['name'] + "\"]/table[@name=\"" + tables['name'] + "\"]/item/data"

                        # finally get the data for each table 
                        # and corresponding table entries 
                        for data in tree.iterfind(path2):
                                for k in xmlfeed:
                                        tmp = k.split('_')
                                        if str(tmp[0]) == str(zones['name']) and str(tmp[1]) == str(tables['name']) and int(tmp[2]) == int(data.attrib['id']): 
                                                data.text = xmlfeed[k]
                                                tree = ET.ElementTree(root)
                                                with open("updated.xml", "w") as f:
                                                        tree.write(f)


def main(domains):
	global domain
	for domain in sorted(domains.iterkeys()):
		
		print "\n##############" ,domain   

		get_auth_data = get_authoritative_nameserver_data()
		#log('%s is authoritative for %s' % (authority, domain))
		# TODO dnssecZoneGlobalAuthNSAddress -->  _dnssecZoneGlobalTable_9 (IpAddress)
		#IMPLEMENT!
		log('dnssecZoneGlobalAuthNSAddress in _dnssecZoneGlobalTable_8 is %s' % (get_auth_data[0]))
		xmlfeed[str(domain + "_dnssecZoneGlobalTable_8")] = '"' + str(get_auth_data[0]) + '"'

		# TODO dnssecZoneGlobalAuthNSName --> _dnssecZoneGlobalTable_10	(OctetString)
		#IMPLEMENT!
		log('dnssecZoneGlobalAuthNSName in _dnssecZoneGlobalTable_10 is %s' % (get_auth_data[1]))
                xmlfeed[str(domain + "_dnssecZoneGlobalTable_9")] = '"' + str(get_auth_data[1]) + '"'

		get_all_authserver = get_all_authoritative_nameservers()
		nameserverlist = ' '.join(get_all_authserver[0])
		#  dnssecZoneAuthNSName -->  _ dnssecZoneAuthNSTable_2 (OctetString)
                log('dnssecZoneAuthNSName in _dnssecZoneAuthNSTable_2 is %s' % (nameserverlist))
                xmlfeed[str(domain + "_dnssecZoneAuthNSTable_2")] = '"' + str(nameserverlist) + '"'
		#  dnssecZoneGlobalAuthNSCount -->  _ dnssecZoneAuthNSTable_2 (Integer32)
                log('dnssecZoneGlobalAuthNSCount in _dnssecZoneGlobalTable_7 is %s' % (get_all_authserver[1]))
                xmlfeed[str(domain + "_dnssecZoneGlobalTable_7")] = str(get_all_authserver[1]) 


		get_soa_data = get_soa()
                # dnssecZoneGlobalSOA -->  _dnssecZoneGlobalTable_11 (DisplayString)
		# TODO _dnssecZoneGlobalTable_13 (OctetString)
                log('dnssecZoneGlobalSOA in _dnssecZoneGlobalTable_12 is %s' % (get_soa_data[0]))
		xmlfeed[str(domain + "_dnssecZoneGlobalTable_12")] = '"' + str(get_soa_data[0]) + '"'
		# dnssecZoneGlobalSOATTL -->  _dnssecZoneGlobalTable_10 (Integer32)
                # TODO _dnssecZoneGlobalTable_12
                log('dnssecZoneGlobalSOATTL in _dnssecZoneGlobalTable_11 is %s' % (get_soa_data[1]))
                xmlfeed[str(domain + "_dnssecZoneGlobalTable_11")] = str(get_soa_data[1])

		validate_dnskey_data = validate_dnskey()
		# dnssecZoneGlobalDNSKEYSignatureVerification -->  _dnssecZoneGlobalTable_6 (Integer32)
                log('dnssecZoneGlobalDNSKEYSignatureVerification in _dnssecZoneGlobalTable_6 is %s' % (validate_dnskey_data))
                xmlfeed[str(domain + "_dnssecZoneGlobalTable_6")] = str(validate_dnskey_data)
	
		minimum_ttl_data = minimum_ttl()
		# TODO dnssecZoneGlobalMinimumTTL -->  _dnssecZoneGlobalTable_11 (Integer32)
                log('dnssecZoneGlobalMinimumTTL in _dnssecZoneGlobalTable_10 is %s' % (minimum_ttl_data))
                xmlfeed[str(domain + "_dnssecZoneGlobalTable_10")] = str(minimum_ttl_data)

		get_origin_recordcount_data = get_origin_recordcount()
		#return zone.origin, totalrecords, totalrecordsets, totaldelegations
		#  dnssecZoneGlobalOrigin -->  _dnssecZoneGlobalTable_2 (OctetString)
                log('dnssecZoneGlobalOrigin in _dnssecZoneGlobalTable_2 is %s' % (get_origin_recordcount_data[0]))
                xmlfeed[str(domain + "_dnssecZoneGlobalTable_2")] = '"' + str(get_origin_recordcount_data[0]) + '"'
		#   dnssecZoneGlobalRecordCount -->  _dnssecZoneGlobalTable_3 (Integer32)
                log('dnssecZoneGlobalRecordCount in _dnssecZoneGlobalTable_3 is %s' % (get_origin_recordcount_data[1]))
                xmlfeed[str(domain + "_dnssecZoneGlobalTable_3")] = str(get_origin_recordcount_data[1]) 
		#   dnssecZoneGlobalRecordSetCount -->  _dnssecZoneGlobalTable_4 (Integer32)
                log('dnssecZoneGlobalRecordSetCount in _dnssecZoneGlobalTable_4 is %s' % (get_origin_recordcount_data[2]))
                xmlfeed[str(domain + "_dnssecZoneGlobalTable_4")] = str(get_origin_recordcount_data[2])
		#   dnssecZoneGlobalDelegationCount -->  _dnssecZoneGlobalTable_5 (Integer32)
                log('dnssecZoneGlobalDelegationCount in _dnssecZoneGlobalTable_5 is %s' % (get_origin_recordcount_data[3]))
                xmlfeed[str(domain + "_dnssecZoneGlobalTable_5")] = str(get_origin_recordcount_data[3])

		editXML()

#stub to launch main
if __name__ == '__main__':
    main(domains)
