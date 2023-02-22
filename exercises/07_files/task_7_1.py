#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
outp = '\n{:12} {}' * 5
with open('ospf.txt') as f:
    for line in f:
        line = line.replace(',', '').replace('[', '').replace(']', '').split()
        print(outp.format(
                'Pref: ', line[1],
                'Metr: ', line[2],
                'NHop: ', line[4],
                'LUpd: ', line[5],
                'OInt: ', line[6]))


