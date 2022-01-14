#/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
access and trunk config ports generator script

there are few vlans and cases for command maybe in trunk port
therefore, according to each port there is a list
and 1st (0) list item set vlan type for vlan number:
	add - for add vlan (switchport trunk allowed vlan add 10,20)
	del - for del vlan from allowed list (switchport trunk allowed vlan remove 17)
	only - only the specified vlans should be set (switchport trunk allowed vlan 11,30)

for pors 0/1, 0/2, 0/4 task:
- generate a configuration based on a template trunk_template
- by keywords: add, del, only

Код не должен привязываться к конкретным номерам портов. То есть, если в словаре
trunk будут другие номера интерфейсов, код должен работать.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

access_template = [
    'switchport mode access', 'switchport access vlan',
    'spanning-tree portfast', 'spanning-tree bpduguard enable'
]

trunk_template = [
    'switchport trunk encapsulation dot1q', 'switchport mode trunk',
    'switchport trunk allowed vlan'
]

access = {
    '0/12': '10',
    '0/14': '11',
    '0/16': '17',
    '0/17': '150'
}
trunk = {
        '0/1': ['add', '10', '20'],
        '0/2': ['only', '11', '30'],
        '0/4': ['del', '17']
    }

trunk_actions = {"add": " add", "del": " remove", "only": ""}

for intf, vlan in access.items():
    print('interface FastEthernet' + intf)
    for command in access_template:
        if command.endswith('access vlan'):
            print(' {} {}'.format(command, vlan))
        else:
            print(' {}'.format(command))

for intf, value in trunk.items():
    print(f"interface FastEthernet {intf}")

    for command in trunk_template:
        if command.endswith("allowed vlan"):
            action = value[0]
            vlans = ",".join(value[1:])
            print(f" {command}{trunk_actions[action]} {vlans}")
        else:
            print(f" {command}")
