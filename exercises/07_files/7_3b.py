#!/usr/bin/env python
u_vlan = input('vlan: \n')
with open('CAM_table.txt') as f:
    for line in f:
        line = line.split()
        if line and line[0] == u_vlan:
            print(f'{line[0]:<4} {line[1]:17} {line[3]}')