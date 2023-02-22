# -*- coding: utf-8 -*-
"""
Задание 19.4

Создать функцию send_commands_to_devices, которая отправляет команду show или config
на разные устройства в параллельных потоках, а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* filename - имя файла, в который будут записаны выводы всех команд
* show - команда show, которую нужно отправить (по умолчанию, значение None)
* config - команды конфигурационного режима, которые нужно отправить (по умолчанию None)
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Аргументы show, config и limit должны передаваться только как ключевые. При передачи
этих аргументов как позиционных, должно генерироваться исключение TypeError.

In [4]: send_commands_to_devices(devices, 'result.txt', 'sh clock')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-4-75adcfb4a005> in <module>
----> 1 send_commands_to_devices(devices, 'result.txt', 'sh clock')

TypeError: send_commands_to_devices() takes 2 positional argument but 3 were given


При вызове функции send_commands_to_devices, всегда должен передаваться
только один из аргументов show, config. Если передаются оба аргумента, должно
генерироваться исключение ValueError.


Вывод команд должен быть записан в файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Пример вызова функции:
In [5]: send_commands_to_devices(devices, 'result.txt', show='sh clock')

In [6]: cat result.txt
R1#sh clock
*04:56:34.668 UTC Sat Mar 23 2019
...
R3#sh clock
*04:56:40.354 UTC Sat Mar 23 2019

In [11]: send_commands_to_devices(devices, 'result.txt', config='logging 10.5.5.5')

In [12]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.5.5.5
R1(config)#end
R1#
...
config term
...
R3(config)#end
R3#

In [13]: commands = ['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']

In [13]: send_commands_to_devices(devices, 'result.txt', config=commands)

In [14]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#router ospf 55
R1(config-router)#network 0.0.0.0 255.255.255.255 area 0
R1(config-router)#end
R1#
...
config term
...
R3(config-router)#end
R3#

"""

import yaml
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from datetime import datetime as dt

logging.basicConfig(format='%(threadName)s %(levelname)s: %(message)s', level=logging.INFO)
logging.getLogger('paramiko').setLevel(logging.WARNING)

connect_msg = '{} ===> {} connect'
receive_msg = '{} <=== {} receive'

def mono_send_show(dev, cmd):
    host = dev['host']
    logging.info(connect_msg.format(dt.now().time(), host))
    try:
        with ConnectHandler(**dev) as ssh:
            ssh.enable()
            return f'show: {host} {cmd}:\n{ssh.send_command(cmd)}\n'
            logging.info(receive_msg.format(dt.now().time(), host))
    except NetmikoTimeoutException:
        return f'{host}: time out'
    except NetmikoAuthenticationException:
        return f'{host}: auth fail'


def mono_send_cfgs(dev, cmd):
    host = dev['host']
    logging.info(connect_msg.format(dt.now().time(), host))
    try:
        with ConnectHandler(**dev) as ssh:
            ssh.enable()
        return f'cfg: {host} {cmd}:\n{ssh.send_config_set(cmd)}\n'
        logging.info(receive_msg.format(dt.now().time(), host))
    except NetmikoTimeoutException:
        return f'{host}: time out\n'
    except NetmikoAuthenticationException:
        return f'{host}: auth fail\n'

def mono_send_all(dev, *, sh=None, cfg=None):
    result = ''
    cmd = sh if sh else cfg
    host = dev['host']
    if type(cmd) == 'str':
        cmd = [cmd]
    logging.info(connect_msg.format(dt.now().time(), host))
    try:
        with ConnectHandler(**dev) as ssh:
            ssh.enable()
            if sh:
                for cmd in cmd:
                    result += f'{host} {cmd}:\n{ssh.send_command(cmd)}\n'
                    logging.info(receive_msg.format(dt.now().time(), host))
                return result
            elif cfg:
                return f'{host} {cmd}:\n{ssh.send_config_set(cmd)}\n'
                logging.info(receive_msg.format(dt.now().time(), host))
    except NetmikoTimeoutException:
        return f'{host}: time out\n'
    except NetmikoAuthenticationException:
        return f'{host}: auth fail\n'

def stereo_send_min(devs, file, *, sh=None, cfgs=None, limit=3):
    if sh and cfgs: raise ValueError('only one of args show/cfgs needed - not both')
    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = [executor.submit(mono_send_all, dev, sh, cfgs) for dev in devs]
        with open(file, 'w') as f:
            for future in as_completed(futures):
                f.write(future.result())

def stereo_send(devs, file, *, show=None, cfgs=None, limit=3):
    if show and cfgs: raise ValueError('only one of args show/cfgs needed - not both')

    cmd = show if show else cfgs
    function = mono_send_show if show else mono_send_cfgs

    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = [executor.submit(function, dev, cmd) for dev in devs]
        with open(file, 'w') as f:
            for future in as_completed(futures):
                f.write(future.result())

show_cmd = 'sh clock'
cfgs_cmd = ['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']

if __name__ == '__main__':
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    stereo_send(devices, 'task_19_4-sh.result', show=show_cmd)
    stereo_send(devices, 'task_19_4-sh.result', cfgs=cfgs_cmd)
    # stereo_send_min(devices, 'task_19_4-sh.result', cfgs=cfgs_cmd)