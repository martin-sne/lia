#!/usr/bin/python
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, tostring, XML
from xml.dom import minidom

#Creation of XML file
xml_file = open("data.xml", "w")


#Zones declaration
zone = ["warsaw.practicum.os3.nl", "derby.practicum.os3.nl", "berlin.warsaw.practicum.os3.nl", "paris.derby.practicum.os3.nl"]
created_zones = []
# Create top of document
top = Element('ZoneList')


# Defines formatting
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")



# Create zones
i=0

def create_zone(zone_name):
        global i
        i = i + 1
        new_zone = SubElement(top, 'Zone', name=zone_name, id=str(i))
        created_zones.append(new_zone)

for zones in zone:
        create_zone(zones)



for zones in created_zones:
	#Create tables
	table1 = SubElement(zones, 'table', name='dnssecGlobalZoneTable')
	table2 = SubElement(zones, 'table', name='dnssecZoneAuthNsTable')
	table3 = SubElement(zones, 'table', name='dnssecZoneSigTable')
	table4 = SubElement(zones, 'table', name='dnssecZoneDiffTable')

	#Create items for table1
	table1_item1 = SubElement(table1, 'item')
	table1_item11 = SubElement(table1_item1, 'data',  id='2', name='dnssecGlobalZoneName', type='DomainOctetString')	
	table1_item2 = SubElement(table1, 'item')
	table1_item22 = SubElement(table1_item2, 'data',  id='3', name='dnssecZoneGlobalRecordCount', type='Gauge32')
	table1_item3 = SubElement(table1, 'item')
	table1_item33 = SubElement(table1_item3, 'data',  id='4', name='dnssecZoneGlobalRecordSetCount', type='Gauge32')
	table1_item4 = SubElement(table1, 'item')
	table1_item44 = SubElement(table1_item4, 'data',  id='5', name='dnssecZoneGlobalDelegationCount', type='Gauge32')
	table1_item5 = SubElement(table1, 'item')
	table1_item55 = SubElement(table1_item5, 'data',  id='6', name='dnssecZoneGlobalRRSigningEnabled', type='CustomInteger')
	table1_item6 = SubElement(table1, 'item')
	table1_item66 = SubElement(table1_item6, 'data',  id='7', name='dnssecZoneGlobalDSValidated', type='CustomInteger')
	table1_item7 = SubElement(table1, 'item')
	table1_item77 = SubElement(table1_item7, 'data',  id='8', name='dnssecZoneGlobalAuthNsCount', type='Gauge32')
	table1_item8 = SubElement(table1, 'item')
	table1_item88 = SubElement(table1_item8, 'data',  id='9', name='dnssecZoneGlobalMinimumTtl', type='TimeInterval')
	table1_item9 = SubElement(table1, 'item')
	table1_item99 = SubElement(table1_item9, 'data',  id='10', name='dnssecZoneGlobalSoaTtl', type='TimeInterval')


	#Create items for table2
	table2_item1 = SubElement(table2, 'item')
	table2_item11 = SubElement(table2_item1, 'data',  id='2', name='dnssecZoneAuthNsName', type='DomainOctetString')
	
	#Create items for table3
	table3_item1 = SubElement(table3, 'item')
	table3_item11= SubElement(table3_item1, 'data',  id='2', name='dnssecZoneSigOldSignatureTime', type='DisplayString')
	table3_item2 = SubElement(table3, 'item')
	table3_item22= SubElement(table3_item2, 'data',  id='3', name='dnssecZoneSigSoaSignatureTime', type='DisplayString')
	table3_item3 = SubElement(table3, 'item')	
	table3_item33= SubElement(table3_item3, 'data',  id='4', name='dnssecZoneSigOpenDnssecPolicyTime', type='TimeInterval')
	table3_item4 = SubElement(table3, 'item')
	table3_item44= SubElement(table3_item4, 'data',  id='5', name='dnssecZoneSigOpenDnssecPolicyOffsetTime', type='TimeInterval')
	table3_item5 = SubElement(table3, 'item')
	table3_item55= SubElement(table3_item5, 'data',  id='6', name='dnssecZoneSigSignaturesTotal', type='Gauge32')
	table3_item6 = SubElement(table3, 'item')
	table3_item66= SubElement(table3_item6, 'data',  id='7', name='dnssecZoneSigValidationErrors', type='Gauge32')
	table3_item7 = SubElement(table3, 'item')
	table3_item77= SubElement(table3_item7, 'data',  id='8', name='dnssecZoneSigVerifiedSignatures', type='Gauge32')

	#Create items for table4
	table4_item1 = SubElement(table4, 'item')
	table4_item11 = SubElement(table4_item1, 'data',  id='2', name='dnssecZoneDiffSerial', type='CustomInteger')
	table4_item2 = SubElement(table4, 'item')
	table4_item22 = SubElement(table4_item2, 'data',  id='3', name='dnssecZoneDiffKsk', type='CustomInteger')
	table4_item3 = SubElement(table4, 'item')	
	table4_item33 = SubElement(table4_item3, 'data',  id='4', name='dnssecZoneDiffZsk', type='CustomInteger')
	table4_item4 = SubElement(table4, 'item')
	table4_item44 = SubElement(table4_item4, 'data',  id='5', name='dnssecZoneDiffRrsig', type='CustomInteger')
	table4_item5 = SubElement(table4, 'item')
	table4_item55 = SubElement(table4_item5, 'data',  id='6', name='dnssecZoneDiffDs', type='CustomInteger')
	



xml_file.write(prettify(top))
xml_file.close()




