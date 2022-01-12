#!usr/bin/env python
# -*- coding: utf-8 -*-
'''
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса. Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой,
   - каждое число в диапазоне от 0 до 255.

Если адрес задан неправильно, выводить сообщение:
'Неправильный IP-адрес'

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''
ip = input("ip: ")

# ip = "10.9.21.250"
check_ip = True

octets = ip.split('.')
if len(octets) != 4:
    check_ip = False
else:
    for octet in octets:
        if not (octet.isdigit() and int(octet) in range(256)):
            check_ip = False
            break
if not check_ip:
    print('ip is not correct. ')
else:
    if ip == '255.255.255.255':
        print('local broadcast')
    elif ip == '0.0.0.0':
        print('unassigned')
    elif int(octets[0]) in range(1, 223):
        print('unicast')
    elif int(octets[0]) in range(224, 240):
        print('multicast')
    else:
        print('unused')
