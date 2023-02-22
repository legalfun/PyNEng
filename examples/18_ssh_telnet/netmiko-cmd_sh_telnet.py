#!/usr/bin/env python3

import netmiko
from pprint import pprint

def send_sh_cmd(params, cmds):
    result = {}
    if type(cmds) == str:
        cmds = [cmds]
    try:
        with netmiko.ConnectHandler(**params) as t:
            t.enable()
            for cmd in cmds:
                result[cmd] = t.send_command(cmd)
            return result
    except netmiko.NetmikoTimeoutException:
        print(f'Connection {params["host"]} failed')
    except netmiko.NetmikoAuthenticationException:
        print(f'Authentication {params["host"]} failed')

cmds = ['sh ip int br', 'sh clock']
device = {
    "device_type": "cisco_ios_telnet",
    "host": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
    "timeout": 2
}

if __name__ == '__main__':
    pprint(send_sh_cmd(device, cmds), width=120)