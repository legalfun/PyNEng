#!/usr/bin/env python
with open('CAM_table.txt') as i_file:
    for line in i_file:
        line = line.split()
        if line and line[0].isdigit():
            metr, mac, *others, intf = line
            print(f'{metr:12} {mac:24} {intf:12}')
