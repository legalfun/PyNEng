#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
mac is list of mac addresses as XXXX:XXXX:XXXX.
In cisco MAC-addresses used as XXXX.XXXX.XXXX.

script convert MAC-addresses to cisco format in list mac_cisco

'''

mac = ['aabb:cc80:7000', 'aabb:dd80:7340', 'aabb:ee80:7000', 'aabb:ff80:7000']
mac_cisco = []
for m in mac:
    mac_cisco.append(m.replace(':', '.'))
print(mac_cisco)
