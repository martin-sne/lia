#!/usr/bin/env python
import dns.resolver
import dns.zone
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, tostring, XML
from xml.dom import minidom
import xml.etree.cElementTree as ET
import re

dnssecZoneSigTable = ["dnssecZoneSigOldSignatureExpirationTime", "dnssecZoneSigSOASignatureExpirationTime", "dnssecZoneSigNSSignatureExpirationTime", "dnssecZoneSigDNSKEYSignatureExpirationTime", "dnssecZoneSigSignaturesTotal"]#, "dnssecZoneSigValidationErrors", "dnssecZoneSigVerifiedSignatures"]


zone = ["warsaw.practicum.os3.nl", "derby.practicum.os3.nl"]


values = {}


def get_data(zone):
	z = dns.zone.from_xfr(dns.query.xfr(zone, zone))
	names = z.nodes.keys()
	names.sort()
	for n in names:
		return z[n].to_text(n)


def oldest_sig(zones):
	data = get_data(zones)
	oldest_rrsig = re.findall(r'RRSIG \w [0-9] [0-9] [0-9]+ [0-9]+ [0-9]+',data)
	dates_rrsig = []
	for values in oldest_rrsig:
		values_list = values.split()
		dates_rrsig.append(values_list[6])
	return dates_rrsig[0]	

def soa_sig_exp(zones):
	data=get_data(zones)
	soa_sig=re.findall(r'RRSIG SOA [0-9] [0-9] [0-9]+ [0-9]+',data)
	dates_soa=[]
	for values in soa_sig:
		values_list=values.split()
		dates_soa.append(values_list[5])
	return dates_soa[0]
	

def ns_sig_exp(zones):
	data=get_data(zones)
        ns_sig=re.findall(r'RRSIG NS [0-9] [0-9] [0-9]+ [0-9]+',data)
        dates_ns=[]
        for values in ns_sig:
        	values_list=values.split()
                dates_ns.append(values_list[5])
	return dates_ns[0]

def dnskey_sig_exp(zones):
	data=get_data(zones)
        dnskey_sig=re.findall(r'RRSIG DNSKEY [0-9] [0-9] [0-9]+ [0-9]+',data)
        dates_dnskey=[]
        for values in dnskey_sig:
	      	values_list=values.split()
        	dates_dnskey.append(values_list[5])
     	return dates_dnskey[0]
		

def sig_total(zones):
	data=get_data(zones)
        return len(re.findall(r'RRSIG',data))


#construct dictionary
for zones in zone:
	print get_data(zones)
