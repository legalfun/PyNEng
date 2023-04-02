# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""

from textfsm import clitable
import netmiko
from pprint import pprint
import yaml
import os

def parse_command_dynamic(
    command_output, attributes_dict, index_file="index", templ_path="templates"
):

    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output, attributes_dict)
    return [dict(zip(cli_table.header, row)) for row in cli_table]

def send_and_parse_show_command(
        device_dict, command, templates_path='templates', index='index'):
    with netmiko.ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        output = ssh.send_command(command, use_textfsm=True)

    # output =
    attributes = {"Command": command, "Vendor": device_dict["device_type"]}
    cli_table = clitable.CliTable(index, templates_path)
    headers =
    result = cli_table.ParseCmd(output, attributes)
    return [dict(zip(headers, list)) for list in result]

if __name__ == '__main__':
    r1_params = {
        "device_type": "cisco_ios",
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
if __name__ == "__main__":
    full_pth = os.path.join(os.getcwd(), "templates")
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        result = send_and_parse_show_command(
            dev, "sh ip int br", templates_path=full_pth
        )
        pprint(result, width=120)
