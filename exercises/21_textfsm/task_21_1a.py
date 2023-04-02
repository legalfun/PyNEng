# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""

import textfsm
from pprint import pprint

# def parse_command_output(template, command_output):
#     with open(template) as tmpl:
#         fsm = textfsm.TextFSM(tmpl)
#         header = fsm.header
#         result = fsm.ParseText(command_output)
#     return [dict(zip(header, line)) for line in result]

def parse_command_output(template, command_output):
    with open(template) as template:
        fsm = textfsm.TextFSM(template)
    return fsm.ParseTextToDicts(command_output)

if __name__ == '__main__':
    with open('output/sh_ip_int_br.txt') as src:
        pprint(parse_command_output('templates/sh_ip_int_br.template', src.read()))