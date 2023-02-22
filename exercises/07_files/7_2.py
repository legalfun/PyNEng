#!/usr/bin/env pyton
with open 'CAM_table' as f:
    for line in f:
        line.split()
        if line and line[0][1].isdigit():
            print(f'{line[0]:<6} {line[1]:24} {line[3]}'

