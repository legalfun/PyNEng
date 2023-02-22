#!/usr/bin/env python3

import netmiko
from pprint import pprint

def send_sh_cmd(dev, user, passw, secret, cmd, dev_type='cisco_ios', time=2):
    try:
        with netmiko.ConnectHandler(device_type=dev_type, host=dev, username=user,
                                    password=passw, secret=secret, timeout=time) as ssh:
            ssh.enable()
            result = ssh.send_command(cmd)
            return result
    except netmiko.NetmikoTimeoutException:
        print(f'Connection to {dev} failed')
    except netmiko.NetMikoAuthenticationException:
        print(f'Authentication to {dev} failed'
              )

if __name__ == '__main__':
    devs = ['192.168.100.1', '192.168.100.2', '192.168.100.3', '192.168.100.4']
    user = passw = secret = 'cisco'
    cmd = 'sh clock'
    for dev in devs:
        out = send_sh_cmd(dev, user, passw, secret, cmd)
        if out:
            pprint(out, width=120)
        else: continue
