#!/bin/sh
while [ true ]; do
 # do what you need to here
 /usr/bin/python /opt/agent/data_wrapper_JN.py
 /usr/bin/python /opt/agent/data_wrapper_ML.py
 sleep 20
done

