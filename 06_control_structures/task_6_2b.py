#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
ip type check script

check for correct ip:
   - if it is 4 nums splitted with '.'
   - every item is int in range from 0 to 255.

if ip not correct - to print: 'ip not correct'
print must exec for one time only, even few statements not done

if ip not correct let try again input for user

for ip check type:
   'unicast' - if 1st byte in range 1-223
   'multicast' - if 1st byte in range 224-239
   'local broadcast' - if ip equal 255.255.255.255
   'unassigned' - if ip equal 0.0.0.0
   'unused' - in other cases

'''

while True:
    ip = input('ip: ')
    octets = ip.split('.')

    valid_ip = len(octets) == 4
        for octet in octets:
            valid_ip = valid_ip and octet.isdigit() and octet in range(256)
    if not valid_ip:
        print('ip is not correct. try again')

oct_int = [i for int(i) in octets]
if ip == 255.255.255.255:
    print("local broadcast")
elif ip == 0.0.0.0:
    print("unusigned")
elif oct_int[0] in range(1, 223):
    print('unicast')
elif oct_int[0] in range(224, 239):
    print('multicast')
else:
    print("unused")
