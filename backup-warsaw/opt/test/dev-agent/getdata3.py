#!/usr/bin/env python
# Inspiration http://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree

import xml.etree.cElementTree as ET
tree = ET.ElementTree(file='data.xml')
root = tree.getroot()
zones_registered = []

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

                                if zones['id'] in zones_registered:
                                        print "Zone ID " + zones['id'] + "already registered"
                                else:
                                        zones_registered.append(zones['id'])
                                        x = tables['name'] + "Row" + zones['id']

                                        #exec (mapping[x] + "=" + tables['name'] + " .addRow([agent.OctetString(" + zones['name'] + ")])")

                                         
                                        y = tables['name'] + ".addRow([agent.OctetString(\"" + zones['name'] + "\")])"
                                        print x + "=" + y
                                        #temp = tables['name'] + "Row" + zones['id'] + "=" + tables['name'] + " .addRow([agent.OctetString(" + zones['name'] + ")])"
                                        #exec (temp)

                                # e.g. dnssecZoneAuthNsTableRow2.setRowCell(2, agent.DisplayString("ns1.distributed-systems.net"))
                                        #exec (tables['name'] + "Row" + zones['id'] + '.setRowCell(' + data.attrib['id'] + ', agent.' + data.attrib['type'] + '(' + data.text + '))')

