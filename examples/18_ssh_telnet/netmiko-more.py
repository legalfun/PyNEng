#!/usr/bin/env python3

import netmiko
import yaml

def send_cmd(params, command):
    if type(command) == 'str':
        command = [command]
    out = ""
    try:
        with netmiko.ConnectHandler(**params) as ssh:
            ssh.enable()
            prompt = ssh.find_prompt()
            ssh.send_command("terminal length 100")
            ssh.write_channel(f"{command}\n")
            while True:
                page = ssh.read_until_pattern(f"More|{prompt}")
                out += page
                if "More" in page:
                    ssh.write_channel(" ")
                elif prompt in page:
                    break
    except netmiko.NetmikoTimeoutException:
        print(f"timeout, {params['host']}")
    except netmiko.NetmikoAuthenticationException:
        print(f"authentication, {params['host']}")
    return out

if __name__ == '__main__':
    cmd = 'sh run'
    with open('devices.yaml') as f:
        settings = yaml.safe_load(f)
    print(send_cmd(settings[0], cmd))
