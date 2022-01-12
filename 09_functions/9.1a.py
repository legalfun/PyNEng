# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 22:08:59 2021

@author: vs
"""

def access_config_generator(intf_vlan_mapping, config_template, pseq=None):
    access_config = []
    for intf, vlan in intf_vlan_mapping.items():
        access_config.append(f'interface {intf}')
        for command in config_template:
            if command.endswith('access vlan'):
                access_config.append(f'{command} {vlan}')
            else:
                access_config.append(command)
        if pseq:
            access_config.extend(pseq)
    return access_config

access_mode_template = [
    "switchport mode access", "switchport access vlan",
    "switchport nonegotiate", "spanning-tree portfast",
    "spanning-tree bpduguard enable"
]

access_config = {
    "FastEthernet0/12": 10,
    "FastEthernet0/14": 11,
    "FastEthernet0/16": 17
}

port_security_template = [
    "switchport port-security maximum 2",
    "switchport port-security violation restrict",
    "switchport port-security",
]

print(access_config_generator(access_config, access_mode_template, port_security_template))
