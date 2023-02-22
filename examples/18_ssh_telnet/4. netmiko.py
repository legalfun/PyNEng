#!/usr/bin/env python3

import pprint
import yaml
import netmiko
from pprint import pprint
from netmiko import (ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException)

time_out = {'timeout': 2}
auth = {'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'
        }
ssh_device_type = {'device_type': 'cisco_ios',}
telnet_device_type = {'device_type': 'cisco_ios_telnet',}

r1 = {'host': '192.168.100.1'}
r2 = {'host': '192.168.100.2'}
r3 = {'host': '192.168.100.3'}

def send_shows(device, cmds):
    result = {}
    if type(cmds) == 'str':
        cmd = [cmds]
    print(f'{device["host"]}: ')
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for cmd in cmds:
                result[cmd] = ssh.send_command(cmd)
        return result

    except NetmikoTimeoutException:
        print(f'timeout for device: {device["host"]}')
    except NetmikoAuthenticationException:
        print(f'failed auth for device: {device["host"]}')

def send_cfgs(device, cmds):
    print(f"{device['host']}: ")
    result = ""
    if type(cmds) == 'str':
        cmds = [cmds]
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result += ssh.config_mode()
            for cmd in cmds:
                output = ssh.send_config_set(cmd, exit_config_mode=False)
                if "%" in output:
                    raise ValueError(f"Command {cmd} failed")
                result += output
            result += ssh.exit_config_mode()
            return result.replace("\r\n", "\n")
    except NetmikoTimeoutException:
        print(f'timeout for device: {device["host"]}')
    except NetmikoAuthenticationException:
        print(f'failed auth for device: {device["host"]}')

show = 'sh clock'
shows = ['sh clock', 'sh ip int br']
cfg = ''
cfgs = {
    "192.168.100.1": ["int lo9", "ipaddress 10.90.90.1 255.255.255.255"],
    "192.168.100.2": ["int lo9"],
    "192.168.100.3": ["int lo9"],
}

if __name__ == '__main__':
# for params in script:
#     for device in r1, r2, r3:
#         output = send_show({**ssh_device_type, **device, **auth, **time_out}, shows)
#         if output:
#             pprint(output, width=120)

# for params in file:
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
        for device in devices:
            try:
                output = send_cfgs(device, cfgs[device['host']])
                if output:
                    pprint(output, width=120)
            except ValueError as error:
                print(error)



