#!/usr/bin/env python
#
# python-netsnmpagent example agent with threading
#
# Copyright (c) 2013 Pieter Hollants <pieter@hollants.com>
# Licensed under the GNU Public License (GPL) version 3
#

#
# simple_agent.py demonstrates registering the various SNMP object types quite
# nicely but uses an inferior control flow logic: the main loop blocks in
# net-snmp's check_and_process() call until some event happens (eg. SNMP
# requests need processing). Only then will data be updated, not inbetween. And
# on the other hand, SNMP requests can not be handled while data is being
# updated, which might take longer periods of time.
#
# This example agent uses a more real life-suitable approach by outsourcing the
# data update process into a separate thread that gets woken up through an
# SIGALRM handler at an configurable interval. This does only ensure periodic
# data updates, it also makes sure that SNMP requests will always be replied to
# in time.
#
# Note that this implementation does not address possible locking issues: if
# a SNMP client's requests are processed while the data update thread is in the
# midst of refreshing the SNMP objects, the client might receive partially
# inconsistent data. 
#
# Use the included script run_threading_agent.sh to test this example.
#
# Alternatively, see the comment block in the head of simple_agent.py for
# adaptable instructions how to run this example against a system-wide snmpd
# instance.
#

import sys, os, signal, time
import optparse, threading, subprocess
import xml.etree.cElementTree as ET
# Make sure we use the local copy, not a system-wide one
sys.path.insert(0, os.path.dirname(os.getcwd()))
import netsnmpagent


prgname = sys.argv[0]
# Process command line arguments
parser = optparse.OptionParser()
parser.add_option(
	"-i",
	"--interval",
	dest="interval",
	help="Set interval in seconds between data updates",
	default=30
)
parser.add_option(
	"-m",
	"--mastersocket",
	dest="mastersocket",
	help="Sets the transport specification for the master agent's AgentX socket",
	default="/var/run/agentx/master"
)
parser.add_option(
	"-p",
	"--persistencedir",
	dest="persistencedir",
	help="Sets the path to the persistence directory",
	default="/var/lib/net-snmp"
)
(options, args) = parser.parse_args()

headerlogged = 0
def LogMsg(msg):
	""" Writes a formatted log message with a timestamp to stdout. """

	global headerlogged

	if headerlogged == 0:
		print "{0:<8} {1:<90} {2}".format(
			"Time",
			"MainThread",
			"UpdateSNMPObjsThread"
		)
		print "{:-^120}".format("-")
		headerlogged = 1

	threadname = threading.currentThread().name

	funcname = sys._getframe(1).f_code.co_name
	if funcname == "<module>":
		funcname = "Main code path"
	elif funcname == "LogNetSnmpMsg":
		funcname = "net-snmp code"
	else:
		funcname = "{0}()".format(funcname)

	if threadname == "MainThread":
		logmsg = "{0} {1:<112.112}".format(
			time.strftime("%T", time.localtime(time.time())),
			"{0}: {1}".format(funcname, msg)
		)
	else:
		logmsg = "{0} {1:>112.112}".format(
			time.strftime("%T", time.localtime(time.time())),
			"{0}: {1}".format(funcname, msg)
		)
	print logmsg

def LogNetSnmpMsg(priority, msg):
	""" Log handler for log messages generated by net-snmp code. """

	LogMsg("[{0}] {1}.".format(priority, msg))

# Create an instance of the netsnmpAgent class
try:
	agent = netsnmpagent.netsnmpAgent(
		AgentName      = "PrototypeAgent",
		MasterSocket   = options.mastersocket,
		PersistenceDir = options.persistencedir,
		MIBFiles       = [ os.path.abspath(os.path.dirname(sys.argv[0])) +
		                   "/ARPA2-Experimental-DNSSEC-MIBv1.txt" ],
		LogHandler     = LogNetSnmpMsg,
	)
except netsnmpagent.netsnmpAgentException as e:
	print "{0}: {1}".format(prgname, e)
	sys.exit(1)


#### Edit ####

# actual data we want to feed the MIB

# TODO
dnsseczonecount = 1

dnssecZoneCount = agent.Unsigned32(
	oidstr = "ARPA2-Experimental-DNSSEC-MIBv1::arpa2experimentaldnssecMIBv1",
	initval = 0,
	writable = False
)
# Create the first table
dnssecZoneGlobalTable = agent.Table(
        oidstr = "ARPA2-Experimental-DNSSEC-MIBv1::dnssecZoneGlobalTable",
        indexes = [
                agent.OctetString()
        ],
        columns = [
		(2, agent.Integer32()),
                (3, agent.OctetString("")),
                (4, agent.Unsigned32(0)),
		(5, agent.Unsigned32(0)),
		(6, agent.Unsigned32(0)),
		(7, agent.Integer32(0)),
		(8, agent.Integer32(0)),
		(9, agent.Unsigned32(0)),
		(10, agent.DisplayString("")),
		(11, agent.OctetString("")),
		(12, agent.Integer32(0)),
		(13, agent.Integer32(0)),
		(14, agent.Integer32(0)),
		(15, agent.DisplayString(""))
        ]

)

# Create the second table

dnssecZoneAuthNSTable = agent.Table(
        oidstr = "ARPA2-Experimental-DNSSEC-MIBv1::dnssecZoneAuthNSTable",
        indexes = [
		agent.OctetString(),
		agent.Unsigned32()
        ],
        columns = [
                (2, agent.DisplayString(""))
        ]
)


# Create the third table
dnssecZoneSigTable = agent.Table(
        oidstr = "ARPA2-Experimental-DNSSEC-MIBv1::dnssecZoneSigTable",
        indexes = [
                agent.OctetString()
        ],
        columns = [
                (2, agent.DisplayString("")),
                (3, agent.DisplayString("")),
                (4, agent.DisplayString("")),
                (5, agent.DisplayString(""))
        ]

)


# Create the fourth table
dnssecZoneDiffTable = agent.Table(
        oidstr = "ARPA2-Experimental-DNSSEC-MIBv1::dnssecZoneDiffTable",
        indexes = [
                agent.OctetString()
        ],
        columns = [
                (2, agent.Integer32(3))
        ]

)


def UpdateSNMPObjs():
	""" Function that does the actual data update. """
	global i
	global dnsseczonecount
	filename='updated.xml'

	LogMsg("Beginning data update.")
	data = ""

	LogMsg("Loading dnssecZoneCount")

	msg = "Updating \"dnssecZoneCount\" ."

	LogMsg("Loading data to feed the MIB")
	tree = ET.ElementTree(file=filename)
	root = tree.getroot()

	# get all zones
	
	counter=0	
	for child_of_root in root:
		counter += 1
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

			if i == 1:
                                x = tables['name'] + "Row" + zones['id']
                                y = tables['name'] + ".addRow([agent.OctetString(\"" + zones['name'] + "\")])"

                                # Register table rows
                                # Example: dnssecGlobalTableRow1=dnssecGlobalTable.addRow([agent.OctetString("os3.nl")])

                                exec("%s = %s" % (x,y))
                                msg = "Registering row " + x + ": " + y
                                LogMsg(msg.format(data))

                        else:
				if counter == 1:	
                                	x = tables['name'] + "Row" + zones['id']
                                	y = tables['name'] + ".clear()"
		
					exec("%s = %s" % (x,y))
                        	        msg = "Clearing row " + x + ": " + y
                                	LogMsg(msg.format(data))


                                x = tables['name'] + "Row" + zones['id']
                                y = tables['name'] + ".addRow([agent.OctetString(\"" + zones['name'] + "\")])"

                                # ReRegister table rows
                                # Example: dnssecGlobalTableRow1=dnssecGlobalTable.addRow([agent.OctetString("os3.nl")])

                                exec("%s = %s" % (x,y))
                                msg = "Registering row " + x + ": " + y
                                LogMsg(msg.format(data))

                	# finally get the data for each table 
                	# and corresponding table entries 
                	for data in tree.iterfind(path2):

                        	exec (tables['name'] + "Row" + zones['id'] + '.setRowCell(' + data.attrib['id'] + ', agent.' + data.attrib['type'] + '(' + data.text + '))')
				msg = "Updating \"" + data.attrib['name']  + "\" in table \"" + tables['name']  + "\" object with data \"" + data.text + "\"."
				LogMsg(msg.format(data))

	LogMsg("Data update done, exiting thread.")

def UpdateSNMPObjsAsync():
	""" Starts UpdateSNMPObjs() in a separate thread. """

	# UpdateSNMPObjs() will be executed in a separate thread so that the main
	# thread can continue looping and processing SNMP requests while the data
	# update is still in progress. However we'll make sure only one update
	# thread is run at any time, even if the data update interval has been set
	# too low.
	global i
	if threading.active_count() == 1:
		LogMsg("Creating thread for UpdateSNMPObjs().")
		t = threading.Thread(target=UpdateSNMPObjs, name="UpdateSNMPObjsThread")
		t.daemon = True
		t.start()
		i += 1
	else:
		LogMsg("Data update still active, data update interval too low?")

# Start the agent (eg. connect to the master agent).
try:
	agent.start()
except netsnmpagent.netsnmpAgentException as e:
	LogMsg("{0}: {1}".format(prgname, e))
	sys.exit(1)

# Trigger initial data update.
LogMsg("Doing initial call to UpdateSNMPObjsAsync().")
i=0
UpdateSNMPObjsAsync()

# Install a signal handler that terminates our threading agent when CTRL-C is
# pressed or a KILL signal is received
def TermHandler(signum, frame):
	global loop
	loop = False
signal.signal(signal.SIGINT, TermHandler)
signal.signal(signal.SIGTERM, TermHandler)

# Define a signal handler that takes care of updating the data periodically
def AlarmHandler(signum, frame):
	global loop, timer_triggered

	LogMsg("Got triggered by SIGALRM.")

	if loop:
		timer_triggered = True

		UpdateSNMPObjsAsync()

		signal.signal(signal.SIGALRM, AlarmHandler)
		signal.setitimer(signal.ITIMER_REAL, float(options.interval))
msg = "Installing SIGALRM handler triggered every {0} seconds."
msg = msg.format(options.interval)
LogMsg(msg)
signal.signal(signal.SIGALRM, AlarmHandler)
signal.setitimer(signal.ITIMER_REAL, float(options.interval))

# The threading agent's main loop. We loop endlessly until our signal
# handler above changes the "loop" variable.
LogMsg("Now serving SNMP requests, press ^C to terminate.")

loop = True
while loop:
	# Block until something happened (signal arrived, SNMP packets processed)
	timer_triggered = False
	res = agent.check_and_process()
	if res == -1 and not timer_triggered and loop:
		loop = False
		LogMsg("Error {0} in SNMP packet processing!".format(res))
	elif loop and timer_triggered:
		LogMsg("net-snmp's check_and_process() returned due to SIGALRM (res={0}), doing another loop.".format(res))
	elif loop:
		LogMsg("net-snmp's check_and_process() returned (res={0}), doing another loop.".format(res))

LogMsg("Terminating.")
agent.shutdown()
