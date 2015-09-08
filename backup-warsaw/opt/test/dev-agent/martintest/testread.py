#!/usr/bin/env python

d = {}
with open("zone_hint") as f:
    for line in f:
       (key, val) = line.split()
       d[str(key)] = val

print d

