#!/usr/bin/env python
ignore=["duplex","alias","configuration"]
from sys import argv
i_file, o_file = argv[1], argv[2]
with open(i_file) as i_f, open(o_file, 'w') as o_f:
    for line in i_f:
        if (not line.startswith('!')) and not (set(line.split()) & set(ignore)):
                o_f.write(line)
                print(line.rstrip())
