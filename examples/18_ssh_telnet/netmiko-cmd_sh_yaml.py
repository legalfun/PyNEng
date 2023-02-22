#!/usr/bin/env python3

import yaml
from pprint import pprint
import netmiko

def send_sh_cmd(device_params, cmds):
    result = {}
    try:
        with netmiko.ConnectHandler(**device_params) as ssh:
            ssh.enable()
            if type(cmds) == 'str':
                cmds = [cmds]
            for cmd in cmds:
                result[cmd] = ssh.send_command(cmd)
        return result
    except netmiko.NetmikoTimeoutException:
        print(f"Connection {device_params['host']} failed")
    except netmiko.NetmikoAuthenticationException:
        print(f"Authentication {device_params['host']} failed")

if __name__ == '__main__':
    cmd = ['sh clock', 'sh ip int br']
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
        for dev in devices:
            pprint(send_sh_cmd(dev, cmd), width=120)
