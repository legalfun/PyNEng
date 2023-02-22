#!/usr/bin/env python
out = '\n{:12} {}' * 5
with open('ospf.txt') as f:
    for line in f:
        line = line.replace(',','').replace('[','').replace(']','')
        line = line.split()
        print(out.format(
            'Prefix:', line[1],
            'Metric:', line[2],
            'N. Hop:', line[4],
            'L. Upd:', line[5],
            'O. Int:', line[6]))

